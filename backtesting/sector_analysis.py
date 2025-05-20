import numpy as np
import pandas as pd
import os

def map_sectors(df: pd.DataFrame) -> dict:
    columns = df.columns[1:]
    sector_map = {}

    for col in columns:
        name = col.upper()
        if any(k in name for k in ["CORN", "SOYBEAN", "WHEAT", "COCOA", "COFFEE", "COTTON", "SUGAR", "CATTLE", "HOG"]):
            sector_map[col] = "Agri & Livestock"
        elif any(k in name for k in ["BRENT", "WTI", "GASOLINE", "HEATING", "NATURAL GAS", "OIL"]):
            sector_map[col] = "Energy"
        elif any(k in name for k in ["GOLD", "SILVER", "PLATINUM", "COPPER", "NICKEL", "ALUMINIUM", "LEAD", "ZINC"]):
            sector_map[col] = "Metals"
        else:
            sector_map[col] = "Other"
    return sector_map

def compute_sector_contributions(df: pd.DataFrame, results_df: pd.DataFrame, sector_map: dict,
                                  output_dir: str = "results") -> pd.DataFrame:
    os.makedirs(output_dir, exist_ok=True)

    relevant_dates = results_df["Date"][results_df["GMM_Filtered"].notna()].reset_index(drop=True)
    sector_returns = {"Agri & Livestock": [], "Energy": [], "Metals": []}

    for date in relevant_dates:
        idx = df.index[df["Date"] == date][0]
        for asset in df.columns[1:]:
            if asset not in sector_map:
                continue
            if idx < 252 or pd.isna(df.loc[idx, asset]) or pd.isna(df.loc[idx - 1, asset]) or pd.isna(df.loc[idx - 252, asset]):
                continue
            if df.loc[idx, asset] > df.loc[idx - 252, asset]:
                daily_return = (df.loc[idx, asset] - df.loc[idx - 1, asset]) / df.loc[idx - 1, asset] * 100
                if not np.isnan(daily_return):
                    sector_returns[sector_map[asset]].append(daily_return)

    avg_sector_contrib = {sector: np.mean(ret) for sector, ret in sector_returns.items()}
    total = sum(avg_sector_contrib.values())
    sector_share = {k: v / total for k, v in avg_sector_contrib.items()}

    sector_df = pd.DataFrame({
        "Sector": sector_share.keys(),
        "Contribution (%)": [round(100 * v, 2) for v in sector_share.values()]
    })

  
    csv_path = os.path.join(output_dir, "sector_contribution.csv")
    txt_path = os.path.join(output_dir, "sector_contribution.txt")
    sector_df.to_csv(csv_path, index=False)

 
    summary_lines = ["Sector Contribution Summary:\n"]
    for row in sector_df.itertuples(index=False):
        summary_lines.append(f"- {row.Sector}: {row._1}% of total return")
    summary_lines.append("\nDiversification across sectors likely contributed to improved risk-adjusted performance.\n")

    with open(txt_path, "w") as f:
        f.write("\n".join(summary_lines))

    print(f" Sector summary saved to: {csv_path} and {txt_path}")
    return sector_df
