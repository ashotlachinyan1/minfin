# armbudget-etl

ETL for the ArmBudget portal: crawl → parse → load → validate → export.
See `../PROJECT_SPEC.md` (sections 5–7) and `../CLAUDE.md` for the rules.

```
uv sync
uv run armbudget --help
uv run pytest
```
