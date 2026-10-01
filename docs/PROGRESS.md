# PROGRESS

## 2026-10-01 — Phase 0: skeleton

### Done
- Spec files committed to repo root: `PROJECT_SPEC.md`, `CLAUDE.md`, `PHASE_PROMPTS.md`, `seed/headline_facts.json`.
- `etl/`: `uv` project (Python 3.12), package `armbudget_etl` with the stage folders from spec 5.3,
  `typer` CLI `armbudget` with `crawl`, `ingest-manual`, `parse`, `load`, `validate`, `export` stubs (exit 1)
  and two working commands: `version`, `check-seed`.
- `web/`: Next.js 15.5 (App Router, static export), TypeScript strict, Tailwind 4, `next-intl` 4 with
  `hy` (default), `ru`, `en`; placeholder home page and the trilingual footer disclaimer from spec 8.
- `Makefile` with targets from CLAUDE.md plus `lint`; `.github/workflows/ci.yml` (lint + test + build on PR).
- `config/thresholds.yaml` (status, reconciliation, identity tolerances from spec 3.3, 7.1, 7.2),
  `config/units.yaml` (unit factors; header markers left empty until real documents are parsed).
- `docs/adr/ADR-001-stack.md`.

### Checks
| Check | Result |
|---|---|
| `make setup` | pass |
| `make lint` (ruff, ruff format, mypy --strict, eslint, tsc, prettier) | pass |
| `make test` (pytest 9, vitest 5) | pass |
| `make web` → `web/out/{hy,ru,en}/index.html` with matching `<html lang>` | pass |
| `/` → `/hy/` meta-refresh redirect present in `out/index.html` | pass |
| ESLint rejects a hardcoded JSX string (manual negative check) | pass |
| `make validate` | fails by design: `validate` is a phase 2 stub |
| GitHub Actions CI | not run yet (runs when a PR is opened) |

Seed arithmetic quoted in the spec was re-checked by tests: implied 2026 GDP (537/0.045 = 11 933;
3 090/0.259 = 11 931; 3 630/0.304 = 11 941 bn AMD, all within 0.5% of 11 930), interest/revenue
420/3 090 = 13.6%, implied USD/AMD 5 300/13.91 = 381.0 → 5 116/13.90 = 368.1 (−3.4%), financing 210 + 327 = 537.

### Open questions (spec 16)
1. Domain and brand (working name ArmBudget); repository is currently named `minfin`.
2. Who reviews the program crosswalk (phase 6).
3. Community budgets in MVP or not.
4. Personal or institutional project — also decides the copyright holder for the MIT `LICENSE`, which is not added yet.

### Next step
Phase 1 — crawler and source inventory (`PHASE_PROMPTS.md`). Expect minfin.am TLS handshake failures;
if the fallback context does not help, files go to `data/manual_drop/` by hand.
