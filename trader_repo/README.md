
# trader

Expert-grade research, backtesting, walk-forward analysis and live paper trading for US equities.

## Why GitHub not OneDrive?
Use **GitHub** for version control, CI, issues and collaboration. OneDrive is fine for sharing files, not code.

## Quickstart (Python 3.11, using uv)

```bash
# 1) Install uv (https://docs.astral.sh/uv/)
pip install uv
# 2) Sync deps
uv sync --all-extras
# 3) Configure environment
cp .env.example .env
# 4) Run a quick backtest on free Yahoo data
uv run trader backtest run --strategy sma_crossover --symbols AAPL MSFT --start 2018-01-01
# 5) Open report
uv run trader report show --path reports/latest.html
```

Alternative with Poetry works as pyproject is standard.

### Config
- Secrets in `.env`
- Runtime in `config/settings.yaml`

### CLI
```bash
trader data fetch --symbols AAPL MSFT --start 2015-01-01
trader backtest run --strategy sma_crossover --symbols AAPL MSFT --start 2015-01-01
trader tune run --strategy rsi_reversion --n-trials 20
trader wf run --strategy vol_breakout --scheme rolling --window 2y --step 3m
trader live run --strategy sma_crossover
trader report show --path reports/latest.html
```

### Acceptance checks
```bash
uv run python scripts/run_backtest.py --strategy sma_crossover
uv run python scripts/run_live.py --strategy sma_crossover  # DRY_RUN by default
pytest -q
ruff check . && black --check .
```

### Notes
- Default data source: Yahoo (yfinance). No keys needed.
- Reports saved under `reports/{timestamp}/...`
- Deterministic: set `seed` in `config/settings.yaml`.

_Generated: 2025-08-30 21:00:30 UTC_
