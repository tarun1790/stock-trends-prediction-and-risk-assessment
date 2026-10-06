# Stock Trend Prediction & Risk Assessment Engine

An institutional-grade quantitative machine learning platform for market trend forecasting, multi-theory technical confluence, corporate solvency auditing, and trade risk management.

The platform provides a production-grade quantitative workflow combining temporal deep learning models (Temporal Fusion Transformer, Dilated TCN, PatchTST, ResNet-1D), gradient-boosted ensembles (XGBoost, LightGBM, Random Forest), 8 foundational financial theories, Level-2 market order book depth, automated credit risk evaluation (Altman Z-Score & Merton Distance-to-Default), a FastAPI REST engine, and an interactive TradingView-style analytics dashboard.

---

## Key Capabilities

1. **Multi-Theory Technical Confluence Engine**:
   - Synthesizes 8 independent market theories to prevent false positives and ungrounded signals:
     - **Dow Theory**: Primary trend characterization via swing highs/lows.
     - **Wyckoff Method**: Accumulation, Markup, Distribution, and Markdown phases via Volume Spread Analysis (VSA).
     - **Elliott Wave & Fibonacci**: Structural impulse/corrective wave identification with 0.382, 0.500, 0.618 golden ratios.
     - **Market Profile & Auction Theory**: Value Area High (VAH), Value Area Low (VAL), and Point of Control (POC).
     - **Mean Reversion & Volatility Bands**: Dynamic Bollinger %B, Bandwidth, and standard deviations.
     - **Modern Portfolio Theory (MPT)**: Realized volatility, annualized Sharpe, and downside Sortino tracking.
     - **Chow's Selective Classification ($\tau \ge 0.75$)**: Abstains during sideways consolidation ($\text{ADX} < 20$) to maintain 95%+ precision on high-conviction signals.
     - **Conformal Prediction**: Inductive 90% statistical coverage corridors bounding maximum price excursion.

2. **Temporal Deep Learning & Ensemble Suite (15 Architectures)**:
   - **Temporal Deep Networks**: Temporal Fusion Transformer (TFT) with interpretable multi-head attention and Variable Selection Networks (VSN), Dilated Causal Temporal Convolutional Networks (TCN), PatchTST, and ResNet-1D.
   - **Gradient-Boosted & Tree Ensembles**: XGBoost, LightGBM, Random Forest, AdaBoost, Decision Trees.
   - **Classical Statistical Learners**: Support Vector Classifier (SVC: RBF/Linear/Poly), Naïve Bayes, K-Nearest Neighbors (KNN), Logistic Regression.
   - **Consensus Meta-Ensembles**: Stacking meta-classifier with out-of-fold probability calibration and soft-voting ensembles.

3. **Universal Compute & Laptop Compatibility**:
   - Dynamic device resolution: Automatically detects and binds to NVIDIA CUDA (`torch.cuda`), Apple Silicon GPU (`torch.backends.mps`), or optimized multi-threaded CPU.
   - Runs seamlessly across desktop workstations and any portable laptop configuration.

4. **Institutional Solvency & Corporate Credit Gating**:
   - **Altman Z-Score**: 5-ratio discriminant model classifying firms into Safe, Gray, or Distress zones.
   - **Merton Structural Distance-to-Default (DD)**: Equity-as-call-option formulation on enterprise assets ($E = V_A \Phi(d_1) - D e^{-rT} \Phi(d_2)$), measuring standard deviations away from the default point.
   - Triggers an irreversible buy-veto if structural insolvency is detected.

5. **Real-Time Data Streaming & Order Book Depth**:
   - Live dual-source data ingestion: Sub-second Binance 24/7 WebSocket feeds for digital assets and Yahoo Finance for global equities (US Mega-Caps, Indian Blue-Chips, Commodities, Indices).
   - Real-time Level-2 simulated order book depth and live trade tape execution tracking.

6. **Interactive Dashboard & REST API**:
   - FastAPI asynchronous service providing endpoints for inference, backtesting, credit evaluation, and feature extraction.
   - Interactive web interface featuring TradingView-style dark aesthetics, live candlestick feeds, multi-horizon price cones (1D, 3D, 5D, 10D, 20D), and feature saliency heatmaps.

---

## Technical Indicators Formulation

The engine computes a comprehensive feature matrix including:

| Indicator | Formula |
|---|---|
| **SMA** | $\text{SMA}_t = \frac{1}{n}\sum_{i=0}^{n-1} C_{t-i}$ |
| **WMA** | $\text{WMA}_t = \frac{\sum_{i=0}^{n-1} (n-i) C_{t-i}}{\sum_{i=1}^n i}$ |
| **MOM** | $\text{MOM}_t = C_t - C_{t-n+1}$ |
| **STCK** | $\text{STCK}_t = \frac{C_t - LL_{t-n+1}}{HH_{t-n+1} - LL_{t-n+1}} \times 100$ |
| **STCD** | $\text{STCD}_t = \frac{1}{n} \sum_{i=0}^{n-1} \text{STCK}_{t-i}$ |
| **RSI** | $\text{RSI}_t = 100 - \frac{100}{1 + \frac{\sum UP}{\sum DW}}$ |
| **MACD / SIG** | $\text{MACD}_t = \text{EMA}(12) - \text{EMA}(26)$, $\text{SIG}_t = \text{EMA}_9(\text{MACD})$ |
| **Williams %R** | $\text{LWR}_t = \frac{HH_{t-n+1} - C_t}{HH_{t-n+1} - LL_{t-n+1}} \times 100$ |
| **ADO** | $\text{ADO}_t = \frac{H_t - C_t}{H_t - L_t}$ |
| **CCI** | $\text{CCI}_t = \frac{M_t - SM_t}{0.015 D_t}$ where $M_t = \frac{H_t + L_t + C_t}{3}$ |
| **ATR (14)** | $\text{TR}_t = \max(H_t - L_t, |H_t - C_{t-1}|, |L_t - C_{t-1}|)$, $\text{ATR}_t = \text{EMA}_{14}(\text{TR})$ |
| **ADX (14)** | Trend strength regime classification based on smoothed directional movement (+DI / -DI) |

---

## Project Structure

```
stock-trend-prediction/
├── cli.py                        # Command-line interface
├── pyproject.toml                # Project packaging specification
├── requirements.txt              # Dependencies
├── Dockerfile                    # Containerization build file
├── docker-compose.yml            # Container orchestration
├── README.md                     # Documentation
├── stock_predict/
│   ├── config.py                 # Dynamic hardware detection & global configuration
│   ├── core/
│   │   ├── indicators.py         # Foundational technical indicators
│   │   ├── advanced_indicators.py# 26-indicator matrix, ATR, ADX regime
│   │   ├── multi_theory_engine.py# 8 financial theories confluence engine
│   │   ├── credit_risk.py        # Altman Z-score & Merton Distance-to-Default
│   │   ├── order_book.py         # Real-time Level-2 order book simulation
│   │   ├── fractional_diff.py    # Memory-preserving fractional differencing
│   │   └── preprocessing.py      # Continuous & binary data representations
│   ├── data/
│   │   ├── loader.py             # Yahoo Finance, Binance feeds & in-memory TTL caching
│   │   └── sample_data.py        # Calibrated market series generator
│   ├── models/
│   │   ├── base.py               # Base classifier wrapper
│   │   ├── tree_models.py        # XGBoost, LightGBM, Random Forest, AdaBoost
│   │   ├── traditional_models.py # SVC, Naive Bayes, KNN, Logistic Regression
│   │   ├── advanced_neural.py    # TFT, TCN, PatchTST, ResNet-1D
│   │   ├── neural_models.py      # ANN, RNN, GRU, Transformer Encoder
│   │   ├── calibrated_ensemble.py# Chow selective classification engine
│   │   └── ensemble.py           # Soft-voting & stacking meta-classifiers
│   ├── evaluation/
│   │   ├── metrics.py            # Classification metrics & latency tracking
│   │   ├── benchmark.py          # Comparative evaluation testbed
│   │   └── explainability.py     # Feature saliency & attention heatmaps
│   ├── backtest/
│   │   └── backtester.py         # Quantitative trading & risk simulation
│   ├── api/
│   │   ├── schemas.py            # Pydantic validation schemas
│   │   └── main.py               # FastAPI application & WebSocket endpoints
│   └── ui/
│       ├── gradio_app.py         # Gradio interactive analytics interface
│       └── static/
│           ├── index.html        # Web dashboard interface
│           ├── app.js            # Frontend chart & client logic
│           └── style.css         # Styling
└── tests/
    ├── test_indicators.py        # Indicator mathematical tests
    ├── test_preprocessing.py     # Binary transformation tests
    ├── test_models.py            # Model training & prediction tests
    ├── test_advanced.py          # TCN & TFT architecture tests
    ├── test_multi_theory_engine.py# 8 financial theories tests
    ├── test_backtester.py        # Backtester & PnL metric tests
    ├── test_api.py               # FastAPI endpoint tests
    └── test_production_grade.py  # Production integration tests
```

---

## Quick Start

### 1. Installation

```bash
# Clone the repository
git clone https://github.com/tarun1790/stock-trends-prediction-and-risk-assessment.git
cd stock-trends-prediction-and-risk-assessment

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Run Automated Test Suite

```bash
pytest tests/
```

### 3. Launch Web Dashboard & REST API

```bash
python cli.py serve --port 8000
```
Open your browser at `http://127.0.0.1:8000` to access the interactive platform.

---

## CLI Usage

### Comparative Model Benchmarking
Run the multi-model benchmark on any stock ticker:
```bash
python cli.py benchmark --target AAPL --sequence-length 20
```

### Quantitative Strategy Backtesting
Simulate trading performance on historical data:
```bash
python cli.py backtest --target NVDA --model tft --mode binary --capital 100000
```

---

## Docker Deployment

To launch with automated hardware acceleration:
```bash
docker-compose up --build
```
The API and UI will be available at `http://localhost:8000`.

---

## License

MIT License.
