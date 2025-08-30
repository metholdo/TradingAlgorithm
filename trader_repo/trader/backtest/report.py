
from __future__ import annotations
from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import plotly.graph_objects as go
from .metrics import equity_curve

def _monthly_heatmap(returns: pd.Series) -> pd.DataFrame:
    df = returns.copy()
    df.index = pd.to_datetime(df.index)
    tbl = df.groupby([df.index.year, df.index.month]).apply(lambda x: (1+x).prod()-1).unstack().fillna(0.0)
    tbl.index.name = "Year"; tbl.columns = [f"{m:02d}" for m in tbl.columns]
    return tbl

def generate_reports(returns: pd.Series, out_dir: str | Path) -> tuple[str, str]:
    Path(out_dir).mkdir(parents=True, exist_ok=True)
    eq = equity_curve(returns)
    dd = eq / eq.cummax() - 1.0

    pdf_path = str(Path(out_dir) / "tearsheet.pdf")
    with PdfPages(pdf_path) as pdf:
        plt.figure(figsize=(10,4))
        plt.plot(eq.index, eq.values)
        plt.title("Equity Curve")
        plt.tight_layout()
        pdf.savefig(); plt.close()

        plt.figure(figsize=(10,2.5))
        plt.fill_between(dd.index, dd.values, 0, step="pre")
        plt.title("Drawdown")
        plt.tight_layout()
        pdf.savefig(); plt.close()

        heat = _monthly_heatmap(returns)
        plt.figure(figsize=(10,6))
        plt.imshow(heat.values, aspect='auto')
        plt.yticks(range(len(heat.index)), heat.index)
        plt.xticks(range(len(heat.columns)), heat.columns)
        plt.title("Monthly Returns Heatmap")
        plt.colorbar()
        plt.tight_layout()
        pdf.savefig(); plt.close()

    html_path = str(Path(out_dir) / "report.html")
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=eq.index.astype(str), y=eq.values, name="Equity"))
    fig.add_trace(go.Scatter(x=dd.index.astype(str), y=dd.values, name="Drawdown", yaxis="y2"))
    fig.update_layout(title="Equity & Drawdown", yaxis2=dict(overlaying="y", side="right"))
    fig.write_html(html_path, include_plotlyjs="cdn")
    return html_path, pdf_path
