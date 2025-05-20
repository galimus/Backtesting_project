import pandas as pd

def compute_market_factor(df: pd.DataFrame) -> pd.DataFrame:
    df_pct = df.copy()
    df_pct.iloc[:, 1:] = df_pct.iloc[:, 1:].pct_change() * 100
    df_pct["Market Factor"] = df_pct.iloc[:, 1:].mean(axis=1)
    df_market = df_pct[["Date", "Market Factor"]].dropna()
    df_market["Cumulative Return"] = (1 + df_market["Market Factor"] / 100).cumprod()
    return df_market
