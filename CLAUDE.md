# CLAUDE.md — правила работы в репозитории armbudget

Полное ТЗ — `PROJECT_SPEC.md`. Фазы и промпты — `PHASE_PROMPTS.md`. Перед любой фазой перечитай разделы ТЗ, на которые ссылается фаза.

## Непреложные правила данных
1. **Никогда не выдумывай цифры.** Если значение не извлечено из документа, оно не попадает в `fact_*`. Пустое значение лучше неверного.
2. Каждая строка факта содержит `source_id`, а для PDF — ещё `source_page` и `source_table`.
3. Суммы хранятся в AMD (не в тысячах). Исходная единица документа — в `source_unit`. Определение единицы — явное (заголовок таблицы / `config/units.yaml`); если единицу определить нельзя, парсер падает с ошибкой, а не угадывает.
4. Уровень достоверности обязателен: `verified | calc | assumption | estimate | media`.
5. Данные СМИ (`media`) — только в `seed/` и `reconciliation_log`, никогда не подменяют официальные.
6. Расхождение ≥ 5% между источниками → запись `warn` в `reconciliation_log` с гипотезой причины; ≥ 10% → `fail`.
7. Не изменяй `data/raw/` — архив неизменяем. Новые версии файлов → новая папка с датой.
8. Ручные правки — только через `data/manual/*.csv` с колонками `reason, source_url, source_page, editor, date`.

## Сеть и краулинг
- minfin.am может отказывать в TLS-рукопожатии. Разрешён повтор с `ctx.set_ciphers('DEFAULT@SECLEVEL=1')`. **Запрещено** `verify=False` и отключение проверки сертификатов.
- 1 запрос в 2 секунды, соблюдение robots.txt, кэш по ETag.
- Если источник недоступен — останови фазу, опиши проблему и попроси пользователя положить файлы в `data/manual_drop/`. Не ищи зеркала или кэш-копии.

## Код
- Python: 3.12, `uv`, `ruff`, `mypy --strict` для `normalize/` и `validate/`, pytest. Каждый парсер — с фикстурой из реального документа и golden-тестом.
- TypeScript strict, ESLint, Prettier; компоненты графиков получают данные только через типизированные props, без `fetch` внутри графика.
- Все пользовательские строки — через `next-intl`; хардкод строк в JSX запрещён (есть lint-правило).
- Числа форматируются только через `web/lib/format.ts`.
- Архитектурные решения, отличающиеся от ТЗ, — только через новый ADR в `docs/adr/`.

## Рабочий цикл каждой сессии
1. Прочитай раздел ТЗ по фазе и `docs/RECONCILIATION_LOG.md`.
2. Составь план (список задач), затем выполняй.
3. Запусти `make validate` (тождества + контракты + сверка) и тесты.
4. В конце сессии обнови `docs/PROGRESS.md`: что сделано, какие проверки прошли или не прошли, открытые вопросы, следующий шаг.
5. Коммиты — маленькие, осмысленные, по-английски в формате conventional commits.

## Команды
```
make setup        # uv sync + pnpm install
make crawl        # обход источников → data/raw + manifest
make parse        # raw → interim
make load         # interim → warehouse (DuckDB)
make validate     # тождества, pandera, cross-source → RECONCILIATION_LOG.md
make export       # warehouse → data/export + web/public/data
make web          # next build (static export)
make test         # pytest + vitest + playwright
make all          # crawl → parse → load → validate → export → web
```
