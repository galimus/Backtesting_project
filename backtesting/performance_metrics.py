import numpy as np
import pandas as pd

def compute_performance_metrics(results_df: pd.DataFrame) -> pd.DataFrame:
    strategy_names = [
        "12M_Momentum", "MA_Crossover", "Breakout", "Lookback_Straddle", "GMM_Filtered", "XGB_Filtered"
    ]
    comparison = []

    for name in strategy_names:
        series = results_df[name].dropna()
        cumulative = (1 + series / 100).cumprod()
        returns = series / 100
        mean_ret = returns.mean()
        std_ret = returns.std()
        sharpe = mean_ret / std_ret if std_ret != 0 else 0

        roll_max = cumulative.cummax()
        drawdown = cumulative / roll_max - 1
        max_dd = drawdown.min()

        comparison.append({
            "Strategy": name,
            "Mean": mean_ret,
            "Std": std_ret,
            "Sharpe": sharpe,
            "Cumulative Return": cumulative.iloc[-1],
            "Max Drawdown": max_dd
        })

    metrics_df = pd.DataFrame(comparison)
    return metrics_df.round(4).sort_values("Sharpe", ascending=False)
