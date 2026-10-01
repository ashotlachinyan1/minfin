"""Seed structure and the arithmetic quoted in PROJECT_SPEC.md (sections 3.6, 7.2, 14.3)."""

from typing import Any

import pytest

from armbudget_etl.seed import check_headline_facts, load_headline_facts


@pytest.fixture(scope="module")
def facts() -> dict[str, dict[str, Any]]:
    return {f["id"]: f for f in load_headline_facts()["facts"]}


def test_seed_structure() -> None:
    assert check_headline_facts(load_headline_facts()) == []


def test_no_verified_facts_in_seed(facts: dict[str, dict[str, Any]]) -> None:
    # Rule 5 (CLAUDE.md): seed holds media/calc only; verified figures come from parsed documents.
    assert {f["confidence"] for f in facts.values()} <= {"media", "calc"}


def test_implied_gdp_2026(facts: dict[str, dict[str, Any]]) -> None:
    deficit = facts["b2026_law_deficit"]["value"]
    ratios = facts["b2026_law_ratios"]["value"]
    implied = facts["b2026_implied_gdp"]["value"]
    for estimate in (
        deficit / 0.045,
        facts["b2026_law_revenue"]["value"] / (ratios["revenue"] / 100),
        facts["b2026_law_expenditure"]["value"] / (ratios["expenditure"] / 100),
    ):
        assert estimate == pytest.approx(implied, rel=0.005)


def test_interest_to_revenue_2026(facts: dict[str, dict[str, Any]]) -> None:
    ratio = facts["b2026_interest"]["value"] / facts["b2026_law_revenue"]["value"] * 100
    assert ratio == pytest.approx(facts["b2026_interest_to_revenue"]["value"], abs=0.05)


def test_implied_fx_h1_2026(facts: dict[str, dict[str, Any]]) -> None:
    ye, q2 = facts["d2025ye_total"], facts["d2026q2_total"]
    fx_ye = ye["value_amd_bn"] / ye["value_usd_bn"]
    fx_q2 = q2["value_amd_bn"] / q2["value_usd_bn"]
    fx = facts["d_fx_effect_h1_2026"]["value"]
    assert fx_ye == pytest.approx(fx["2025-12-31"], abs=0.1)
    assert fx_q2 == pytest.approx(fx["2026-06-30"], abs=0.1)
    assert (fx_q2 / fx_ye - 1) * 100 == pytest.approx(fx["change_pct"], abs=0.05)


def test_deficit_financing_sums_to_deficit_2026(facts: dict[str, dict[str, Any]]) -> None:
    fin = facts["b2026_deficit_financing"]["value"]
    assert fin["domestic"] + fin["external"] == facts["b2026_law_deficit"]["value"]
