import numpy as np
import pandas as pd
from sklearn.mixture import GaussianMixture
from sklearn.preprocessing import StandardScaler

def apply_gmm_filter(results_df: pd.DataFrame, df_market: pd.DataFrame) -> pd.DataFrame:
    market_for_gmm = df_market[df_market["Date"].isin(results_df["Date"])].copy()
    X_scaled = StandardScaler().fit_transform(market_for_gmm[["Market Factor"]])
    gmm = GaussianMixture(n_components=2, random_state=42)
    gmm.fit(X_scaled)

    regime = gmm.predict(X_scaled)
    means = gmm.means_.flatten()
    trend_label = means.argmax()
    market_for_gmm["Regime"] = (regime == trend_label).astype(int)

    merged = pd.merge(results_df, market_for_gmm[["Date", "Regime"]], on="Date", how="left")
    merged["GMM_Filtered"] = merged["12M_Momentum"] * merged["Regime"]
    merged["Cumulative_GMM_Filtered"] = (1 + merged["GMM_Filtered"] / 100).cumprod()

    return merged
