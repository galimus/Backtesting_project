#  Backtesting Project – Imperial College

I  implemented and compared five trend-following strategies on commodity futures using time-series momentum signals:

- **12M Momentum**
- **Moving Average Crossover**
- **Breakout Signal**
- **Lookback Straddle**
- **GMM-Filtered Momentum** (using Gaussian Mixture Models)

---

##  Project Structure

- `backtesting/` – modular code for data loading, strategies, metrics, regression, and plotting
- `data/` – contains the input Excel file 
- `results/` – automatically generated plots and performance tables
- `run.py` – main script that runs the full backtest
- `run.sh` – bash script to create environment and launch the project
- `requirements.txt` – Python dependencies

---

## How to Run

```bash
bash run.sh
