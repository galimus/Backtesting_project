import pandas as pd

def compute_summary_stats(df: pd.DataFrame) -> pd.DataFrame:
    summary_stats = []
    for col in df.columns[1:]:
        series = df[["Date", col]].dropna()
        stats = {
            "Asset": col,
            "First Date": series["Date"].min().strftime("%Y-%m-%d"),
            "N Observations": series.shape[0],
            "Mean": series[col].mean(),
            "Std Dev": series[col].std(),
            "Min": series[col].min(),
            "Max": series[col].max()
        }
        summary_stats.append(stats)
    summary_df = pd.DataFrame(summary_stats)
    return summary_df.sort_values("Asset").reset_index(drop=True).round(4)
