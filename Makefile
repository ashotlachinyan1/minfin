# ArmBudget — pipeline and build targets (CLAUDE.md "Команды").
ETL := cd etl && uv run
WEB := cd web && pnpm

.PHONY: setup crawl parse load validate export web test lint all

setup:
	cd etl && uv sync
	$(WEB) install --frozen-lockfile

crawl:
	$(ETL) armbudget crawl

parse:
	$(ETL) armbudget parse

load:
	$(ETL) armbudget load

validate:
	$(ETL) armbudget check-seed
	$(ETL) armbudget validate

export:
	$(ETL) armbudget export

web:
	$(WEB) build

lint:
	$(ETL) ruff check .
	$(ETL) ruff format --check .
	$(ETL) mypy
	$(WEB) lint
	$(WEB) typecheck
	$(WEB) format:check

test:
	$(ETL) pytest
	$(WEB) test

all: crawl parse load validate export web
