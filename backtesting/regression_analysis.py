import pandas as pd
import statsmodels.api as sm

def run_regressions(results_df: pd.DataFrame, df_market: pd.DataFrame) -> pd.DataFrame:
    strategy_names = [
        "12M_Momentum", "MA_Crossover", "Breakout", "Lookback_Straddle", "GMM_Filtered", "XGB_Filtered"
    ]
    regression_results = []

    for name in strategy_names:
        df_merged = pd.merge(results_df[["Date", name]], df_market[["Date", "Market Factor"]], on="Date")
        y = df_merged[name].dropna()
        x = df_merged.loc[y.index, "Market Factor"]

        X = sm.add_constant(x)
        model = sm.OLS(y, X).fit()

        regression_results.append({
            "Strategy": name,
            "Alpha": round(model.params["const"], 5),
            "Beta": round(model.params["Market Factor"], 5),
            "R²": round(model.rsquared, 4),
            "p-value (β)": round(model.pvalues["Market Factor"], 4)
        })

    return pd.DataFrame(regression_results)
