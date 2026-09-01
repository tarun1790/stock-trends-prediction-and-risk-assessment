# Stock Market Trend Prediction Platform

An enterprise-grade quantitative machine learning and deep learning platform for financial market trend forecasting, built on the research findings of the IEEE Access publication:

> **"Predicting Stock Market Trends Using Machine Learning and Deep Learning Algorithms Via Continuous and Binary Data; a Comparative Analysis"**  
> *M. Nabipour, P. Nayyeri, H. Jabani, S. Shamshirband, A. Mosavi (IEEE Access, Vol. 8, 2020).*

This repository provides an end-to-end Software Development Life Cycle (SDLC) implementation combining high-performance PyTorch GPU-accelerated deep learning models, tree ensembles, traditional kernel estimators, a quantitative trading backtester, a FastAPI REST service, and an interactive real-time analytical dashboard.

---

## Key Capabilities

1. **Exact 10 IEEE Technical Indicators**:
   - Simple Moving Average (SMA, 10-day)
   - Weighted Moving Average (WMA, 10-day)
   - Momentum (MOM, 10-day)
   - Stochastic Oscillator %K (STCK, 10-day)
   - Stochastic Oscillator %D (STCD, 10-day)
   - Relative Strength Index (RSI, 10-day)
   - MACD Signal Line (SIG, 9-day on 12/26 EMA)
   - Larry Williams %R (LWR, 10-day)
   - Accumulation/Distribution Oscillator (ADO)
   - Commodity Channel Index (CCI, 10-day)

2. **Dual Data Representation Engine**:
   - **Continuous Representation**: Raw indicator values normalized to $[0, 1]$ via MinMax scaling.
   - **Trend-Deterministic Binary Representation**: Domain-specific heuristic rules converting non-stationary oscillators into $+1$ (Upward signal) and $-1$ (Downward signal), mirroring the paper's breakthrough methodology that boosted classification F1 scores from ~68% to ~90%.

3. **15 Machine Learning & Deep Learning Architectures**:
   - **Tree Ensembles**: Decision Tree, Random Forest, AdaBoost, XGBoost, LightGBM.
   - **Traditional Classifiers**: Support Vector Classifier (SVC: RBF/Poly/Linear/Sigmoid), Naïve Bayes, K-Nearest Neighbors (KNN), Logistic Regression.
   - **PyTorch GPU Deep Learning**: Multi-Layer Perceptron (ANN), Recurrent Neural Network (RNN), Long Short-Term Memory (LSTM), Gated Recurrent Unit (GRU), Bidirectional LSTM with Multi-Head Self-Attention, Time-Series Transformer.
   - **Meta Ensembles**: Soft-Voting & Stacking Classifiers.

4. **Quantitative Trading Backtester**:
   - Execution simulation on model prediction signals (+1 Long, 0 Cash / -1 Short).
   - Real-world friction modeling (transaction fees, slippage).
   - Performance metrics: Total Return %, CAGR %, Sharpe Ratio, Sortino Ratio, Max Drawdown %, Win Rate %, Profit Factor, Alpha, and Beta against Buy & Hold benchmark.

5. **Production REST API & Interactive UI Dashboard**:
   - FastAPI server with asynchronous endpoints for data fetching, indicator extraction, model training, benchmarking, inference, and backtesting.
   - Modern, responsive web interface with Chart.js price overlays, binary indicator heatmaps, benchmark bar charts, and live forecast dials.

---

## Technical Indicators Formulation

| Indicator | Formula |
|---|---|
| **SMA** | $\text{SMA}_t = \frac{1}{n}\sum_{i=0}^{n-1} C_{t-i}$ |
| **WMA** | $\text{WMA}_t = \frac{\sum_{i=0}^{n-1} (n-i) C_{t-i}}{\sum_{i=1}^n i}$ |
| **MOM** | $\text{MOM}_t = C_t - C_{t-n+1}$ |
| **STCK** | $\text{STCK}_t = \frac{C_t - LL_{t-n+1}}{HH_{t-n+1} - LL_{t-n+1}} \times 100$ |
| **STCD** | $\text{STCD}_t = \frac{1}{n} \sum_{i=0}^{n-1} \text{STCK}_{t-i}$ |
| **RSI** | $\text{RSI}_t = 100 - \frac{100}{1 + \frac{\sum UP}{\sum DW}}$ |
| **SIG** | $\text{MACD}_t = \text{EMA}(12) - \text{EMA}(26)$, $\text{SIG}_t = \text{EMA}_9(\text{MACD})$ |
| **LWR** | $\text{LWR}_t = \frac{HH_{t-n+1} - C_t}{HH_{t-n+1} - LL_{t-n+1}} \times 100$ |
| **ADO** | $\text{ADO}_t = \frac{H_t - C_t}{H_t - L_t}$ |
| **CCI** | $\text{CCI}_t = \frac{M_t - SM_t}{0.015 D_t}$ where $M_t = \frac{H_t + L_t + C_t}{3}$ |

---

## Project Structure

```
stock-trend-prediction/
├── cli.py                        # Unified command-line interface
├── pyproject.toml                # Project packaging specification
├── requirements.txt              # Production dependencies
├── Dockerfile                    # Containerization build file
├── docker-compose.yml            # Container orchestration with GPU pass-through
├── README.md                     # Documentation
├── stock_predict/
│   ├── config.py                 # Hardware auto-detection & global settings
│   ├── core/
│   │   ├── indicators.py         # 10 technical indicators implementation
│   │   └── preprocessing.py      # Continuous & binary data pipelines
│   ├── data/
│   │   ├── loader.py             # Yahoo Finance, TSE sectors & CSV loader
│   │   └── sample_data.py        # Table 11 calibrated synthetic generator
│   ├── models/
│   │   ├── base.py               # Base classifier wrapper
│   │   ├── tree_models.py        # Decision Tree, RF, AdaBoost, XGBoost, LightGBM
│   │   ├── traditional_models.py # SVC, Naive Bayes, KNN, Logistic Regression
│   │   ├── neural_models.py      # PyTorch CUDA ANN, RNN, LSTM, GRU, BiLSTM, Transformer
│   │   └── ensemble.py           # Soft-Voting & Stacking ensembles
│   ├── evaluation/
│   │   ├── metrics.py            # F1, Accuracy, ROC-AUC, latency calculations
│   │   └── benchmark.py          # Continuous vs Binary benchmark testbed
│   ├── backtest/
│   │   └── backtester.py         # Quantitative trading & risk simulation
│   ├── api/
│   │   ├── schemas.py            # Pydantic schemas
│   │   └── main.py               # FastAPI application & REST routes
│   └── ui/
│       └── static/
│           ├── index.html        # Modern dashboard interface
│           ├── app.js            # Frontend chart & client logic
│           └── style.css         # Styling
└── tests/
    ├── test_indicators.py        # Indicator mathematical tests
    ├── test_preprocessing.py     # Binary transformation tests
    ├── test_models.py            # ML & PyTorch DL training tests
    ├── test_backtester.py        # P&L & risk metric tests
    └── test_api.py               # FastAPI integration tests
```

---

## Quick Start

### 1. Installation

```bash
# Clone the repository
git clone https://github.com/tarun1790/stock-trend-prediction.git
cd stock-trend-prediction

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Run Automated Test Suite

```bash
pytest -v tests/
```

### 3. Launch Web Dashboard & REST API

```bash
python cli.py serve --port 8000
```
Open your browser at `http://127.0.0.1:8000` to access the interactive platform.

---

## CLI Usage

### Comparative Model Benchmarking
Run the 15-model benchmark comparing Continuous vs Binary representations on any sector or stock:
```bash
python cli.py benchmark --target diversified_financials --sequence-length 20
```

### Quantitative Strategy Backtesting
Simulate trading performance on historical data:
```bash
python cli.py backtest --target AAPL --model lstm --mode binary --capital 100000
```

---

## Docker Deployment

To launch with GPU support:
```bash
docker-compose up --build
```
The API and UI will be available at `http://localhost:8000`.

---

## License

MIT License.
