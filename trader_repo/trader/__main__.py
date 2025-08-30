
from __future__ import annotations
import typer
from typing import List
import pandas as pd
from pathlib import Path
from .config import load_settings, Settings
from .data_sources.yahoo import YahooSource
from .data_sources.alpaca import AlpacaSource
from .strategies.sma_crossover import SMACrossover
from .strategies.rsi_reversion import RSIReversion
from .strategies.vol_breakout import VolBreakout
from .backtest.engine import run as run_bt
from .backtest.report import generate_reports

app = typer.Typer(add_completion=False, no_args_is_help=True)

def _get_ds(s: Settings):
    if s.data_source == "yahoo":
        return YahooSource(s)
    if s.data_source == "alpaca":
        return AlpacaSource(s)
    raise typer.BadParameter("Unknown data_source")

def _get_strategy(name: str):
    name = name.lower()
    if name == "sma_crossover":
        return SMACrossover().generate_signals
    if name == "rsi_reversion":
        return RSIReversion().generate_signals
    if name == "vol_breakout":
        return VolBreakout().generate_signals
    raise typer.BadParameter(f"Unknown strategy {name}")

@app.command("data")
def data_fetch(symbols: List[str]=typer.Option(None, help="Symbols"),
               start: str=typer.Option(None, help="Start date YYYY-MM-DD")):
    s = load_settings()
    if symbols: s.symbols = symbols
    ds = _get_ds(s)
    df = ds.fetch_history(s.symbols, start=start or s.start, timeframe=s.timeframe)
    out = Path(s.cache_path); out.mkdir(parents=True, exist_ok=True)
    typer.echo(f"Fetched {len(df)} rows. Cached under {out}")

@app.command("backtest")
def backtest_run(strategy: str=typer.Option("sma_crossover"),
                 symbols: List[str]=typer.Option(None),
                 start: str=typer.Option(None),
                 fees_bps: float=typer.Option(10.0),
                 slippage_bps: float=typer.Option(5.0)):
    s = load_settings()
    if symbols: s.symbols = symbols
    if start: s.start = start
    ds = _get_ds(s)
    df = ds.fetch_history(s.symbols, start=s.start, timeframe=s.timeframe)
    sym = s.symbols[0]
    px = df.reset_index().query("symbol == @sym").set_index("date")["close"].sort_index()
    strat_fn = _get_strategy(strategy)
    sig = strat_fn(px).positions
    res = run_bt(px, sig, fees_bps=fees_bps, slippage_bps=slippage_bps)
    out_dir = Path(s.reports_path) / pd.Timestamp.now().strftime("%Y%m%d_%H%M%S")
    out_dir.mkdir(parents=True, exist_ok=True)
    html, pdf = generate_reports(res.returns, out_dir)
    latest = Path(s.reports_path) / "latest.html"
    latest.write_text(Path(html).read_text(encoding="utf-8"), encoding="utf-8")
    typer.echo(f"Summary: {res.summary}")
    typer.echo(f"Report: {html} | PDF: {pdf}")
    typer.echo(f"Also wrote: {latest}")

@app.command("tune")
def tune_run(strategy: str=typer.Option("sma_crossover"), n_trials: int=typer.Option(20)):
    from .backtest.tuner import optimise
    s = load_settings()
    ds = _get_ds(s)
    df = ds.fetch_history(s.symbols, start=s.start, timeframe=s.timeframe)
    px = df.reset_index().query("symbol == @s.symbols[0]").set_index("date")["close"].sort_index()
    strat_fn = _get_strategy(strategy)
    html = optimise(px, strat_fn, n_trials=n_trials)
    out = Path(s.reports_path) / "tuning.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html, encoding="utf-8")
    typer.echo(f"Wrote {out}")

@app.command("wf")
def wf_run(strategy: str=typer.Option("sma_crossover"), scheme: str=typer.Option("rolling"),
           window: int=typer.Option(504), step: int=typer.Option(63)):
    s = load_settings()
    ds = _get_ds(s)
    df = ds.fetch_history(s.symbols, start=s.start, timeframe=s.timeframe)
    px = df.reset_index().query("symbol == @s.symbols[0]").set_index("date")["close"].sort_index()
    strat_fn = _get_strategy(strategy)
    res = []
    i = 0
    while i + window + step < len(px):
        train = px.iloc[i:i+window]
        test = px.iloc[i+window:i+window+step]
        sig = strat_fn(train).positions
        bt = run_bt(train, sig)
        sig2 = strat_fn(test).positions
        bt2 = run_bt(test, sig2)
        res.append(bt2.summary["sharpe"])
        i += step
    typer.echo(f"OOS Sharpe mean={pd.Series(res).mean():.3f} over {len(res)} windows")

@app.command("live")
def live_run(strategy: str=typer.Option("sma_crossover")):
    from .live.executor import run_live
    run_live(strategy=strategy)

@app.command("report")
def report_show(path: str):
    p = Path(path)
    assert p.exists(), f"{p} not found"
    typer.echo(f"Open: {p.resolve()}")

if __name__ == "__main__":
    app()
