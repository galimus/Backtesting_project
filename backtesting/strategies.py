import numpy as np
import pandas as pd

def compute_strategies(df: pd.DataFrame) -> pd.DataFrame:
    lookback_12m = 252
    ma_fast = 20
    ma_slow = 120
    breakout_window = 60
    lookback_straddle = 60

    returns = df.copy()
    returns.iloc[:, 1:] = returns.iloc[:, 1:].pct_change() * 100
    returns = returns.dropna().reset_index(drop=True)
    dates = returns["Date"]
    assets = df.columns[1:]

    strategies = {"12M_Momentum": [], "MA_Crossover": [], "Breakout": []}

    for i in range(max(lookback_12m, ma_slow, breakout_window), len(returns)):
        daily_returns = {k: [] for k in strategies}
        for asset in assets:
            prices = df[asset].values
            curr_price = prices[i]
            r = returns.loc[i, asset]

            if curr_price > prices[i - lookback_12m]:
                daily_returns["12M_Momentum"].append(r)

            fast_ma = np.mean(prices[i - ma_fast:i])
            slow_ma = np.mean(prices[i - ma_slow:i])
            if fast_ma > slow_ma:
                daily_returns["MA_Crossover"].append(r)

            high_past = np.max(prices[i - breakout_window:i])
            if curr_price > high_past:
                daily_returns["Breakout"].append(r)

        for k in strategies:
            strategies[k].append(np.mean(daily_returns[k]) if daily_returns[k] else 0)

    results_df = pd.DataFrame({
        "Date": dates[max(lookback_12m, ma_slow, breakout_window):],
        "12M_Momentum": strategies["12M_Momentum"],
        "MA_Crossover": strategies["MA_Crossover"],
        "Breakout": strategies["Breakout"]
    })

    for k in strategies:
        results_df[f"Cumulative_{k}"] = (1 + results_df[k] / 100).cumprod()

    # Lookback Straddle
    strategies["Lookback_Straddle"] = []
    for i in range(max(lookback_12m, ma_slow, breakout_window, lookback_straddle), len(returns)):
        daily_ret_ls = []
        for asset in assets:
            prices = df[asset].values
            curr_price = prices[i]
            past_high = np.max(prices[i - lookback_straddle:i])
            past_low = np.min(prices[i - lookback_straddle:i])
            if (curr_price > past_high) or (curr_price < past_low):
                r = returns.loc[i, asset]
                daily_ret_ls.append(r)
        mean_ret = np.mean(daily_ret_ls) if daily_ret_ls else 0
        strategies["Lookback_Straddle"].append(mean_ret)

    padding = len(results_df) - len(strategies["Lookback_Straddle"])
    results_df["Lookback_Straddle"] = [0] * padding + strategies["Lookback_Straddle"]
    results_df["Cumulative_Lookback_Straddle"] = (1 + results_df["Lookback_Straddle"] / 100).cumprod()

    return results_df
