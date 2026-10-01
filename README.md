# ArmBudget

Independent interactive portal for the Republic of Armenia's state budget and public debt:
plan vs actual by program and measure, debt portfolio analytics, every figure linked to its source.

- Specification: [`PROJECT_SPEC.md`](PROJECT_SPEC.md)
- Rules for Claude Code sessions: [`CLAUDE.md`](CLAUDE.md)
- Phase prompts: [`PHASE_PROMPTS.md`](PHASE_PROMPTS.md)
- Progress: [`docs/PROGRESS.md`](docs/PROGRESS.md)

## Quick start (macOS / Linux)
Requires `uv`, Node.js 22 and `pnpm` 10.

```
make setup   # uv sync + pnpm install
make test    # pytest + vitest
make web     # static site → web/out
```
