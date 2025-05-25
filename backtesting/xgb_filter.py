
import pandas as pd
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

def train_xgb_model(df_market_returns, quantile=0.75):
    df = df_market_returns[["Date", "Market Factor"]].copy()
    df["Return"] = df["Market Factor"]
    df["Return_Lag1"] = df["Return"].shift(1)
    df["Vol_5"] = df["Return"].rolling(5).std()
    df["Vol_20"] = df["Return"].rolling(20).std()
    df["Mom_5"] = df["Return"].rolling(5).mean()
    df["Mom_20"] = df["Return"].rolling(20).mean()
    df["MA_diff"] = df["Mom_5"] - df["Mom_20"]
    df.dropna(inplace=True)
    df = df.reset_index(drop=True)

    threshold = df["Return"].quantile(quantile)
    df["Regime"] = (df["Return"] > threshold).astype(int)

    class_balance = df["Regime"].value_counts(normalize=True)
    print("\n[INFO] Class balance:")
    print(class_balance)

    features = ["Return_Lag1", "Vol_5", "Vol_20", "Mom_5", "Mom_20", "MA_diff"]
    X = df[features]
    y = df["Regime"]

    X_train, X_test, y_train, y_test = train_test_split(X, y, shuffle=False, test_size=0.2)
    scale_pos_weight = class_balance[0] / class_balance[1]

    model = xgb.XGBClassifier(
        use_label_encoder=False,
        eval_metric="logloss",
        scale_pos_weight=scale_pos_weight,
        random_state=42
    )
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    print("\n[INFO] Classification report:")
    print(classification_report(y_test, y_pred))

    df["XGB_Regime"] = model.predict(X)
    print("[INFO] XGB_Regime added. Sample:")
    print(df[["Date", "XGB_Regime"]].head())

    return model, df, features

def apply_xgb_filter(results_df, df_xgb, features):
    df_filtered = pd.merge(results_df, df_xgb[["Date", "XGB_Regime"]], on="Date", how="left")
    df_filtered["XGB_Filtered"] = df_filtered["12M_Momentum"] * df_filtered["XGB_Regime"]
    df_filtered["Cumulative_XGB_Filtered"] = (1 + df_filtered["XGB_Filtered"] / 100).cumprod()

    print("[INFO] XGB_Filtered column added to results_df.")
    print(df_filtered[["Date", "XGB_Filtered", "Cumulative_XGB_Filtered"]].tail())

    return df_filtered
