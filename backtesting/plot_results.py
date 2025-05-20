import matplotlib.pyplot as plt
import pandas as pd
import os
from datetime import datetime

def plot_cumulative_returns(results_df: pd.DataFrame, output_dir: str = "results"):
    os.makedirs(output_dir, exist_ok=True)
    file_name = f"strategy_comparison_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
    output_path = os.path.join(output_dir, file_name)

    plt.figure(figsize=(12, 6))
    for name in [
        "Cumulative_12M_Momentum",
        "Cumulative_MA_Crossover",
        "Cumulative_Breakout",
        "Cumulative_Lookback_Straddle",
        "Cumulative_GMM_Filtered"
    ]:
        label = name.replace("Cumulative_", "").replace("_", " ")
        plt.plot(results_df["Date"], results_df[name], label=label)

    plt.title("Cumulative Returns: Strategy Comparison")
    plt.xlabel("Date")
    plt.ylabel("Cumulative Return (×)")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()

    print(f" Plot saved to: {output_path}")
