#  Backtesting Project – Imperial College

I implemented and compared six trend-following strategies on commodity futures using time-series momentum signals:

- **12M Momentum**
- **Moving Average Crossover**
- **Breakout Signal**
- **Lookback Straddle**
- **GMM-Filtered Momentum** (using Gaussian Mixture Models)
- **XGB-Filtered Momentum** (using XGBoost machine learning)

---

##  Project Structure

- `backtesting/` – modular code for data loading, strategies, metrics, regression, and plotting  
- `data/` – contains the input Excel file  
- `results/` – automatically generated plots and performance summaries  
- `run.py` – main script that runs the full backtest  
- `run.sh` – bash script to create environment and launch the project on macOS/Linux  
- `requirements.txt` – Python dependencies

---

## How to Run

###  On macOS / Linux

```bash
bash run.sh
```

---

### On Windows (CMD, PowerShell, or Anaconda Prompt)

Open a terminal (CMD, PowerShell, or Anaconda Prompt) and run:

```bash
cd path\to\Backtesting_project
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python run.py
```

---

## Output

All results are saved to the `results/` folder, including:

- Strategy performance plots (`.png`)  
- Strategy metrics summary (`strategy_metrics_summary.txt`)  
-  Sector contribution summary (`sector_contribution.txt` / `.csv`)
