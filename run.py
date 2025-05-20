import os
import shutil
from backtesting.data_loader import load_returns
from backtesting.summary_stats import compute_summary_stats
from backtesting.market_factor import compute_market_factor
from backtesting.strategies import compute_strategies
from backtesting.regime_filter import apply_gmm_filter
from backtesting.performance_metrics import compute_performance_metrics
from backtesting.regression_analysis import run_regressions
from backtesting.sector_analysis import map_sectors, compute_sector_contributions
from backtesting.plot_results import plot_cumulative_returns

DATA_PATH = "data/Commodities Data thru 15May25.xlsx"

def main():
    results_dir = "results"
    if os.path.exists(results_dir):
        shutil.rmtree(results_dir)
    os.makedirs(results_dir)

    print("Loading data...")
    df = load_returns(DATA_PATH)

    print("Computing summary statistics...")
    summary = compute_summary_stats(df)
    print(summary.head())

    print("Building market factor...")
    df_market = compute_market_factor(df)

    print("Running strategies...")
    results = compute_strategies(df)

    print("Applying GMM regime filter...")
    results = apply_gmm_filter(results, df_market)

    print("Calculating metrics...")
    metrics = compute_performance_metrics(results)
    print(metrics)

    print("Running regressions...")
    reg = run_regressions(results, df_market)
    print(reg)

    print("Sector contribution analysis...")
    sector_map = map_sectors(df)
    sector_df = compute_sector_contributions(df, results, sector_map)
    print(sector_df)

    print("Plotting...")
    plot_cumulative_returns(results)

if __name__ == "__main__":
    main()
