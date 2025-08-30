
from __future__ import annotations
import optuna
import pandas as pd
from typing import Callable, Any
from .engine import run

def optimise(prices: pd.Series, strat_fn: Callable[..., Any], n_trials: int=20) -> str:
    def objective(trial: optuna.Trial) -> float:
        fast = trial.suggest_int("fast", 5, 50)
        slow = trial.suggest_int("slow", 60, 250)
        sig = strat_fn(prices, fast=fast, slow=slow).positions
        res = run(prices, sig)
        return float(res.summary["sharpe"])
    study = optuna.create_study(direction="maximize")
    study.optimize(objective, n_trials=n_trials)
    html = optuna.visualization.plot_optimization_history(study).to_html(full_html=True, include_plotlyjs="cdn")
    return html
