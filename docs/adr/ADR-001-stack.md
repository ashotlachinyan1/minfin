# ADR-001: Technology stack

- Status: accepted
- Date: 2026-10-01
- Context: PROJECT_SPEC.md sections 0.2, 5.1–5.3

## Context
ArmBudget is a static, read-only portal over Armenian state budget and public debt data.
The dominant cost and risk is data extraction and reconciliation (spec 0.2: an estimated 70–80% of effort),
not the frontend. The site has no user accounts and collects no personal data (spec 11).

## Decision
| Layer | Choice | Reason |
|---|---|---|
| ETL language | Python 3.12, managed by `uv` | mature PDF/XLSX/DOCX parsing ecosystem; `uv.lock` gives reproducible installs |
| CLI / orchestration | `typer` CLI behind `make` targets | transparent, no scheduler infrastructure |
| Quality gates (ETL) | `ruff` (lint + format), `mypy --strict`, `pytest`; `pandera` contracts from phase 2 | parser regressions are the top failure scenario (spec 0.3) |
| Storage | DuckDB file → Parquet exports (phase 2) | zero infrastructure, SQL, fast columnar export |
| Frontend | Next.js 15 App Router with `output: "export"`, TypeScript strict, Tailwind CSS 4 | static site, SEO, one page per program via SSG |
| i18n | `next-intl` 4; locales `hy` (default), `ru`, `en` | ICU plurals; works with static export via `generateStaticParams` + `setRequestLocale` |
| Charts | Apache ECharts + d3 for custom views (phase 7+) | treemap/sunburst/sankey/heatmap out of the box |
| Tests (web) | Vitest now; Playwright, Lighthouse CI, axe-core from phase 7/11 | |
| CI | GitHub Actions: lint + test + build on every PR | |
| Hosting | Cloudflare Pages (phase 12) | free static hosting |

## Consequences and deviations noted in phase 0
- **Dependencies are added per phase.** Phase 0 installs only what the skeleton uses (`typer`, `pyyaml`).
  `pandas`/`polars`, `openpyxl`, `pdfplumber`, `camelot`, `python-docx`, `httpx`, `pydantic`, `pandera`, `duckdb`
  are added in the phase that first needs them, so every dependency is exercised by a test when it lands.
- **Root redirect without middleware.** Static export cannot run next-intl middleware, so `/` is a static page
  with `<meta http-equiv="refresh">` to `/hy/`. Phase 12 may add a Cloudflare `_redirects` rule as well.
- **No hardcoded UI strings.** Enforced by ESLint `react/jsx-no-literals` (`noStrings`) on `app/` and `components/`;
  a Vitest test checks that `hy`, `ru`, `en` message files have identical keys and no empty values (spec 14.2).
- **CLI stubs fail.** Unimplemented pipeline commands exit with code 1, so `make all` cannot silently "succeed"
  without producing data.
- **Toolchain pins.** TypeScript is pinned to 5.x (the 7.x native compiler is not supported by Next.js 15's
  build-time type check); ESLint 9 flat config is required by `eslint-config-next` 15.

## Alternatives considered
- Next.js server rendering / API routes: rejected; adds hosting cost and attack surface with no benefit for public data.
- PostgreSQL warehouse: rejected for MVP; DuckDB covers the data volume (≈ 10^5–10^6 rows) with zero ops.
