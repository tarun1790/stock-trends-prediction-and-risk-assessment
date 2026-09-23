"""
Section 3: Database Design Module
"""
try:
    from . import svg_diagrams as svgs
except Exception:
    import svg_diagrams as svgs

def get_section3_html():
    svg_er = svgs.get_er_database_svg()
    template = """
<!-- SECTION 3: DATABASE DESIGN -->
<div class="page-break"></div>
<h2>Section 3: Relational Database Design &amp; Entity Modeling</h2>

<h3>3.1 Database Modeling Methodology &amp; Normalization</h3>
<p>
The AlphaTemporal persistent data store is designed according to strict <strong>Third Normal Form (3NF)</strong> specifications, eliminating data redundancy, update anomalies, and partial/transitive dependencies. Time-series historical bars, technical features, machine learning runs, selective decisions, and trade executions are decoupled into specialized relations linked by immutable foreign key relationships.
</p>

<h3>3.2 Entity-Relationship (ER) Diagram</h3>
<p>
The diagram below presents the complete relational database entity schema, showing primary keys (PK), foreign keys (FK), and cardinalities utilizing formal Crow's Foot notation.
</p>

<div class="diagram-container">
  {svg_er}
</div>

<h3>3.3 Relational Database Tables Specification (12 Tables in 3NF)</h3>

<!-- Table 1: Equities -->
<h4>Table 1: <code>EQUITIES</code> (Master Asset Catalog)</h4>
<table>
  <thead>
    <tr><th>Column Name</th><th>Data Type</th><th>Null?</th><th>Key</th><th>Default</th><th>Description &amp; Business Constraints</th></tr>
  </thead>
  <tbody>
    <tr><td><code>ticker</code></td><td>VARCHAR(16)</td><td>NO</td><td>PK</td><td>&mdash;</td><td>Unique asset symbol (e.g. <code>'TCS.NS'</code>, <code>'NVDA'</code>, <code>'BTC-USD'</code>).</td></tr>
    <tr><td><code>company_name</code></td><td>VARCHAR(128)</td><td>NO</td><td>&mdash;</td><td>&mdash;</td><td>Full legal corporation name or index designation.</td></tr>
    <tr><td><code>exchange</code></td><td>VARCHAR(16)</td><td>NO</td><td>&mdash;</td><td>&mdash;</td><td>Listing exchange: <code>'NSE'</code>, <code>'BSE'</code>, <code>'NASDAQ'</code>, <code>'NYSE'</code>, <code>'CRYPTO'</code>.</td></tr>
    <tr><td><code>sector_key</code></td><td>VARCHAR(64)</td><td>NO</td><td>&mdash;</td><td>&mdash;</td><td>Sector classification key (e.g. <code>'diversified_financials'</code>).</td></tr>
    <tr><td><code>currency</code></td><td>VARCHAR(8)</td><td>NO</td><td>&mdash;</td><td>'$'</td><td>Trading currency symbol: <code>'$'</code>, <code>'&#8377;'</code>, <code>'&#165;'</code>, <code>'&#8364;'</code>.</td></tr>
    <tr><td><code>is_crypto</code></td><td>BOOLEAN</td><td>NO</td><td>&mdash;</td><td>FALSE</td><td>Flag denoting 24/7 continuous continuous trading.</td></tr>
    <tr><td><code>is_active</code></td><td>BOOLEAN</td><td>NO</td><td>&mdash;</td><td>TRUE</td><td>Soft-deletion flag for deprecated or delisted securities.</td></tr>
  </tbody>
</table>

<!-- Table 2: MarketSessions -->
<h4>Table 2: <code>MARKET_SESSIONS</code> (Exchange Operating Clocks)</h4>
<table>
  <thead>
    <tr><th>Column Name</th><th>Data Type</th><th>Null?</th><th>Key</th><th>Default</th><th>Description &amp; Business Constraints</th></tr>
  </thead>
  <tbody>
    <tr><td><code>session_id</code></td><td>BIGINT</td><td>NO</td><td>PK</td><td>AUTO</td><td>Synthetic primary key for trading session instance.</td></tr>
    <tr><td><code>exchange</code></td><td>VARCHAR(16)</td><td>NO</td><td>FK</td><td>&mdash;</td><td>Target exchange operating rules.</td></tr>
    <tr><td><code>trade_date</code></td><td>DATE</td><td>NO</td><td>&mdash;</td><td>&mdash;</td><td>Calendar date of the market session.</td></tr>
    <tr><td><code>open_time_ist</code></td><td>TIME</td><td>NO</td><td>&mdash;</td><td>'09:15:00'</td><td>Session opening clock in Indian Standard Time (IST).</td></tr>
    <tr><td><code>close_time_ist</code></td><td>TIME</td><td>NO</td><td>&mdash;</td><td>'15:30:00'</td><td>Session closing clock in Indian Standard Time (IST).</td></tr>
    <tr><td><code>is_holiday</code></td><td>BOOLEAN</td><td>NO</td><td>&mdash;</td><td>FALSE</td><td>Flag for statutory exchange closures.</td></tr>
    <tr><td><code>closing_cross_frozen</code></td><td>BOOLEAN</td><td>NO</td><td>&mdash;</td><td>FALSE</td><td>Integrity flag confirming post-market price freeze.</td></tr>
  </tbody>
</table>

<!-- Table 3: CandleData_1D -->
<h4>Table 3: <code>CANDLE_DATA_1D</code> (Historical OHLCV Time Series)</h4>
<table>
  <thead>
    <tr><th>Column Name</th><th>Data Type</th><th>Null?</th><th>Key</th><th>Default</th><th>Description &amp; Business Constraints</th></tr>
  </thead>
  <tbody>
    <tr><td><code>candle_id</code></td><td>BIGINT</td><td>NO</td><td>PK</td><td>AUTO</td><td>Monotonically increasing candle identifier.</td></tr>
    <tr><td><code>ticker</code></td><td>VARCHAR(16)</td><td>NO</td><td>FK</td><td>&mdash;</td><td>References <code>EQUITIES.ticker</code> (ON DELETE RESTRICT).</td></tr>
    <tr><td><code>timestamp_utc</code></td><td>DATETIME</td><td>NO</td><td>&mdash;</td><td>&mdash;</td><td>UTC bar closing timestamp. UNIQUE(ticker, timestamp_utc).</td></tr>
    <tr><td><code>open_price</code></td><td>NUMERIC(12,4)</td><td>NO</td><td>&mdash;</td><td>&mdash;</td><td>Opening price of the session. CHECK(open_price &gt; 0).</td></tr>
    <tr><td><code>high_price</code></td><td>NUMERIC(12,4)</td><td>NO</td><td>&mdash;</td><td>&mdash;</td><td>Session high price. CHECK(high_price &gt;= low_price).</td></tr>
    <tr><td><code>low_price</code></td><td>NUMERIC(12,4)</td><td>NO</td><td>&mdash;</td><td>&mdash;</td><td>Session low price. CHECK(low_price &gt; 0).</td></tr>
    <tr><td><code>close_price</code></td><td>NUMERIC(12,4)</td><td>NO</td><td>&mdash;</td><td>&mdash;</td><td>Official closing cross settlement price.</td></tr>
    <tr><td><code>volume</code></td><td>BIGINT</td><td>NO</td><td>&mdash;</td><td>0</td><td>Total shares or contracts traded. CHECK(volume &gt;= 0).</td></tr>
    <tr><td><code>vwap</code></td><td>NUMERIC(12,4)</td><td>YES</td><td>&mdash;</td><td>NULL</td><td>Volume-Weighted Average Price for the session.</td></tr>
    <tr><td><code>data_source</code></td><td>VARCHAR(32)</td><td>NO</td><td>&mdash;</td><td>'YAHOO'</td><td>Origin: <code>'YAHOO'</code>, <code>'BINANCE_WS'</code>, <code>'SYNTHETIC'</code>.</td></tr>
  </tbody>
</table>

<!-- Table 4: FeatureMatrix_26 -->
<h4>Table 4: <code>FEATURE_MATRIX_26</code> (Vectorized Multi-Scale Indicators)</h4>
<table>
  <thead>
    <tr><th>Column Name</th><th>Data Type</th><th>Null?</th><th>Key</th><th>Default</th><th>Description &amp; Business Constraints</th></tr>
  </thead>
  <tbody>
    <tr><td><code>feature_id</code></td><td>BIGINT</td><td>NO</td><td>PK</td><td>AUTO</td><td>Synthetic feature row identifier.</td></tr>
    <tr><td><code>candle_id</code></td><td>BIGINT</td><td>NO</td><td>FK</td><td>&mdash;</td><td>References <code>CANDLE_DATA_1D.candle_id</code> (ON DELETE CASCADE).</td></tr>
    <tr><td><code>hma_9</code></td><td>NUMERIC(12,4)</td><td>NO</td><td>&mdash;</td><td>&mdash;</td><td>1D FIR Vectorized Hull Moving Average (period 9).</td></tr>
    <tr><td><code>supertrend_dir</code></td><td>INT</td><td>NO</td><td>&mdash;</td><td>1</td><td>SuperTrend trailing band state (+1 = Bullish, -1 = Bearish).</td></tr>
    <tr><td><code>adx_14</code></td><td>NUMERIC(6,3)</td><td>NO</td><td>&mdash;</td><td>&mdash;</td><td>Wilder's Directional Movement Index (Regime filter &ge; 22).</td></tr>
    <tr><td><code>rsi_14</code></td><td>NUMERIC(6,3)</td><td>NO</td><td>&mdash;</td><td>&mdash;</td><td>Relative Strength Index (0.0 to 100.0).</td></tr>
    <tr><td><code>macd_line</code></td><td>NUMERIC(8,4)</td><td>NO</td><td>&mdash;</td><td>&mdash;</td><td>MACD Difference: EMA(12) - EMA(26).</td></tr>
    <tr><td><code>macd_signal</code></td><td>NUMERIC(8,4)</td><td>NO</td><td>&mdash;</td><td>&mdash;</td><td>MACD 9-day signal line.</td></tr>
    <tr><td><code>frac_diff_d</code></td><td>NUMERIC(10,5)</td><td>NO</td><td>&mdash;</td><td>&mdash;</td><td>Stationary FFD series (<math xmlns="http://www.w3.org/1998/Math/MathML" display="inline"><mrow><msup><mi>d</mi><mo>&#x0002A;</mo></msup><mo>&#x02248;</mo><mn>0.40</mn></mrow></math>, ADF <math xmlns="http://www.w3.org/1998/Math/MathML" display="inline"><mrow><mi>p</mi><mo>&lt;</mo><mn>0.05</mn></mrow></math>).</td></tr>
    <tr><td><code>other_indicators</code></td><td>JSON</td><td>NO</td><td>&mdash;</td><td>'{}'</td><td>Remaining 19 technical indicators stored as structured payload.</td></tr>
  </tbody>
</table>

<!-- Table 5: ModelRegistry -->
<h4>Table 5: <code>MODEL_REGISTRY</code> (Model Catalog &amp; Metadata)</h4>
<table>
  <thead>
    <tr><th>Column Name</th><th>Data Type</th><th>Null?</th><th>Key</th><th>Default</th><th>Description &amp; Business Constraints</th></tr>
  </thead>
  <tbody>
    <tr><td><code>model_id</code></td><td>VARCHAR(32)</td><td>NO</td><td>PK</td><td>&mdash;</td><td>Unique identifier: <code>'tcn'</code>, <code>'tft'</code>, <code>'bilstm_attention'</code>, <code>'xgboost'</code>.</td></tr>
    <tr><td><code>model_family</code></td><td>VARCHAR(32)</td><td>NO</td><td>&mdash;</td><td>&mdash;</td><td>Classification: <code>'DEEP_LEARNING'</code>, <code>'TREE_ENSEMBLE'</code>, <code>'LINEAR'</code>.</td></tr>
    <tr><td><code>architecture</code></td><td>VARCHAR(64)</td><td>NO</td><td>&mdash;</td><td>&mdash;</td><td>PyTorch class or Scikit-Learn wrapper type.</td></tr>
    <tr><td><code>receptive_field</code></td><td>INT</td><td>NO</td><td>&mdash;</td><td>1</td><td>Historical lookback window in trading days (TCN = 61).</td></tr>
    <tr><td><code>supports_gpu</code></td><td>BOOLEAN</td><td>NO</td><td>&mdash;</td><td>FALSE</td><td>Flag indicating CUDA acceleration compatibility.</td></tr>
    <tr><td><code>param_count</code></td><td>BIGINT</td><td>NO</td><td>&mdash;</td><td>0</td><td>Number of trainable neural weights or tree nodes.</td></tr>
  </tbody>
</table>

<!-- Table 6: ModelTrainingRuns -->
<h4>Table 6: <code>MODEL_TRAINING_RUNS</code> (Walk-Forward Experimentation Registry)</h4>
<table>
  <thead>
    <tr><th>Column Name</th><th>Data Type</th><th>Null?</th><th>Key</th><th>Default</th><th>Description &amp; Business Constraints</th></tr>
  </thead>
  <tbody>
    <tr><td><code>run_id</code></td><td>BIGINT</td><td>NO</td><td>PK</td><td>AUTO</td><td>Unique training run identifier.</td></tr>
    <tr><td><code>model_id</code></td><td>VARCHAR(32)</td><td>NO</td><td>FK</td><td>&mdash;</td><td>References <code>MODEL_REGISTRY.model_id</code>.</td></tr>
    <tr><td><code>ticker</code></td><td>VARCHAR(16)</td><td>NO</td><td>FK</td><td>&mdash;</td><td>Target training equity ticker.</td></tr>
    <tr><td><code>train_epochs</code></td><td>INT</td><td>NO</td><td>&mdash;</td><td>80</td><td>Number of backpropagation epochs executed.</td></tr>
    <tr><td><code>f1_score</code></td><td>NUMERIC(6,4)</td><td>NO</td><td>&mdash;</td><td>&mdash;</td><td>Harmonic mean of precision and recall.</td></tr>
    <tr><td><code>accuracy</code></td><td>NUMERIC(6,4)</td><td>NO</td><td>&mdash;</td><td>&mdash;</td><td>Out-of-sample validation accuracy.</td></tr>
    <tr><td><code>weights_path</code></td><td>VARCHAR(256)</td><td>YES</td><td>&mdash;</td><td>NULL</td><td>Filesystem URI to serialized PyTorch <code>.pt</code> weights.</td></tr>
    <tr><td><code>trained_on_gpu</code></td><td>VARCHAR(32)</td><td>YES</td><td>&mdash;</td><td>NULL</td><td>GPU hardware telemetry signature (e.g. RTX 3070 Ti).</td></tr>
  </tbody>
</table>

<!-- Table 7: InferencePredictions -->
<h4>Table 7: <code>INFERENCE_PREDICTIONS</code> (Raw Multi-Model Class Posteriors)</h4>
<table>
  <thead>
    <tr><th>Column Name</th><th>Data Type</th><th>Null?</th><th>Key</th><th>Default</th><th>Description &amp; Business Constraints</th></tr>
  </thead>
  <tbody>
    <tr><td><code>pred_id</code></td><td>BIGINT</td><td>NO</td><td>PK</td><td>AUTO</td><td>Inference event primary key.</td></tr>
    <tr><td><code>run_id</code></td><td>BIGINT</td><td>NO</td><td>FK</td><td>&mdash;</td><td>References <code>MODEL_TRAINING_RUNS.run_id</code>.</td></tr>
    <tr><td><code>candle_id</code></td><td>BIGINT</td><td>NO</td><td>FK</td><td>&mdash;</td><td>References <code>CANDLE_DATA_1D.candle_id</code>.</td></tr>
    <tr><td><code>prob_up</code></td><td>NUMERIC(6,4)</td><td>NO</td><td>&mdash;</td><td>&mdash;</td><td>Posterior probability <math xmlns="http://www.w3.org/1998/Math/MathML" display="inline"><mrow><mi>P</mi><mo stretchy="false">&#x00028;</mo><mi>Y</mi><mo>&#x0003D;</mo><mtext>Up</mtext><mo>&#x02223;</mo><mi>X</mi><mo stretchy="false">&#x00029;</mo></mrow></math>.</td></tr>
    <tr><td><code>prob_down</code></td><td>NUMERIC(6,4)</td><td>NO</td><td>&mdash;</td><td>&mdash;</td><td>Posterior probability <math xmlns="http://www.w3.org/1998/Math/MathML" display="inline"><mrow><mi>P</mi><mo stretchy="false">&#x00028;</mo><mi>Y</mi><mo>&#x0003D;</mo><mtext>Down</mtext><mo>&#x02223;</mo><mi>X</mi><mo stretchy="false">&#x00029;</mo></mrow></math>.</td></tr>
    <tr><td><code>predicted_class</code></td><td>INT</td><td>NO</td><td>&mdash;</td><td>&mdash;</td><td>Argmax predicted index (1 = Bullish, 0 = Bearish).</td></tr>
    <tr><td><code>inference_latency_ms</code></td><td>NUMERIC(8,2)</td><td>NO</td><td>&mdash;</td><td>0.0</td><td>Forward pass execution latency on CUDA device.</td></tr>
  </tbody>
</table>

<!-- Table 8: ChowSelectiveDecisions -->
<h4>Table 8: <code>CHOW_SELECTIVE_DECISIONS</code> (Optimal Rejection Log)</h4>
<table>
  <thead>
    <tr><th>Column Name</th><th>Data Type</th><th>Null?</th><th>Key</th><th>Default</th><th>Description &amp; Business Constraints</th></tr>
  </thead>
  <tbody>
    <tr><td><code>decision_id</code></td><td>BIGINT</td><td>NO</td><td>PK</td><td>AUTO</td><td>Unique selective decision identifier.</td></tr>
    <tr><td><code>pred_id</code></td><td>BIGINT</td><td>NO</td><td>FK</td><td>&mdash;</td><td>References <code>INFERENCE_PREDICTIONS.pred_id</code> (1:1).</td></tr>
    <tr><td><code>confidence_max</code></td><td>NUMERIC(6,4)</td><td>NO</td><td>&mdash;</td><td>&mdash;</td><td>Max posterior <math xmlns="http://www.w3.org/1998/Math/MathML" display="inline"><mrow><mi>g</mi><mo stretchy="false">&#x00028;</mo><mi>x</mi><mo stretchy="false">&#x00029;</mo><mo>&#x0003D;</mo><msub><mo>max</mo><mi>k</mi></msub><mi>P</mi><mo stretchy="false">&#x00028;</mo><mi>Y</mi><mo>&#x0003D;</mo><mi>k</mi><mo>&#x02223;</mo><mi>X</mi><mo stretchy="false">&#x00029;</mo></mrow></math>.</td></tr>
    <tr><td><code>tau_threshold</code></td><td>NUMERIC(6,4)</td><td>NO</td><td>&mdash;</td><td>0.7500</td><td>Chow rejection threshold <math xmlns="http://www.w3.org/1998/Math/MathML" display="inline"><mrow><mi>&#x003C4;</mi></mrow></math>.</td></tr>
    <tr><td><code>status</code></td><td>VARCHAR(16)</td><td>NO</td><td>&mdash;</td><td>&mdash;</td><td><code>'EXECUTED'</code> (if <math xmlns="http://www.w3.org/1998/Math/MathML" display="inline"><mrow><mi>g</mi><mo stretchy="false">&#x00028;</mo><mi>x</mi><mo stretchy="false">&#x00029;</mo><mo>&#x02265;</mo><mi>&#x003C4;</mi></mrow></math>) or <code>'ABSTAIN_CASH'</code>.</td></tr>
    <tr><td><code>bounded_error</code></td><td>NUMERIC(6,4)</td><td>NO</td><td>&mdash;</td><td>&mdash;</td><td>Theoretical conditional error bound: <math xmlns="http://www.w3.org/1998/Math/MathML" display="inline"><mrow><mn>1</mn><mo>&#x02212;</mo><mi>&#x003C4;</mi><mo>&#x0003D;</mo><mn>0.25</mn></mrow></math>.</td></tr>
    <tr><td><code>is_executed</code></td><td>BOOLEAN</td><td>NO</td><td>&mdash;</td><td>FALSE</td><td>Execution flag routed to capital allocation engine.</td></tr>
  </tbody>
</table>

<!-- Table 9: CreditDistressMetrics -->
<h4>Table 9: <code>CREDIT_DISTRESS_METRICS</code> (Merton &amp; Altman Solvency Logs)</h4>
<table>
  <thead>
    <tr><th>Column Name</th><th>Data Type</th><th>Null?</th><th>Key</th><th>Default</th><th>Description &amp; Business Constraints</th></tr>
  </thead>
  <tbody>
    <tr><td><code>credit_id</code></td><td>BIGINT</td><td>NO</td><td>PK</td><td>AUTO</td><td>Credit evaluation identifier.</td></tr>
    <tr><td><code>ticker</code></td><td>VARCHAR(16)</td><td>NO</td><td>FK</td><td>&mdash;</td><td>References <code>EQUITIES.ticker</code>.</td></tr>
    <tr><td><code>altman_z_score</code></td><td>NUMERIC(8,3)</td><td>NO</td><td>&mdash;</td><td>&mdash;</td><td>Altman 5-factor manufacturing/service Z-Score.</td></tr>
    <tr><td><code>merton_dd</code></td><td>NUMERIC(8,3)</td><td>NO</td><td>&mdash;</td><td>&mdash;</td><td>Physical Distance-to-Default in asset standard deviations.</td></tr>
    <tr><td><code>default_prob_pct</code></td><td>NUMERIC(6,3)</td><td>NO</td><td>&mdash;</td><td>&mdash;</td><td>Structural default probability: <math xmlns="http://www.w3.org/1998/Math/MathML" display="inline"><mrow><mi>&#x003A6;</mi><mo stretchy="false">&#x00028;</mo><mo>&#x02212;</mo><mi>D</mi><mi>D</mi><mo stretchy="false">&#x00029;</mo><mo>&#x000D7;</mo><mn>100</mn></mrow></math>.</td></tr>
    <tr><td><code>distress_zone</code></td><td>VARCHAR(16)</td><td>NO</td><td>&mdash;</td><td>&mdash;</td><td><code>'SAFE_ZONE'</code>, <code>'GREY_ZONE'</code>, <code>'DISTRESS_ZONE'</code>.</td></tr>
    <tr><td><code>buy_veto_flag</code></td><td>BOOLEAN</td><td>NO</td><td>&mdash;</td><td>FALSE</td><td>Irreversible veto: TRUE if <math xmlns="http://www.w3.org/1998/Math/MathML" display="inline"><mrow><mi>Z</mi><mo>&lt;</mo><mn>1.81</mn></mrow></math> or <math xmlns="http://www.w3.org/1998/Math/MathML" display="inline"><mrow><mi>D</mi><mi>D</mi><mo>&lt;</mo><mn>1.5</mn></mrow></math>.</td></tr>
  </tbody>
</table>

<!-- Table 10: TradingActionPlans -->
<h4>Table 10: <code>TRADING_ACTION_PLANS</code> (Institutional Execution Blueprints)</h4>
<table>
  <thead>
    <tr><th>Column Name</th><th>Data Type</th><th>Null?</th><th>Key</th><th>Default</th><th>Description &amp; Business Constraints</th></tr>
  </thead>
  <tbody>
    <tr><td><code>plan_id</code></td><td>BIGINT</td><td>NO</td><td>PK</td><td>AUTO</td><td>Trading plan primary key.</td></tr>
    <tr><td><code>decision_id</code></td><td>BIGINT</td><td>NO</td><td>FK</td><td>&mdash;</td><td>References <code>CHOW_SELECTIVE_DECISIONS.decision_id</code>.</td></tr>
    <tr><td><code>credit_id</code></td><td>BIGINT</td><td>NO</td><td>FK</td><td>&mdash;</td><td>References <code>CREDIT_DISTRESS_METRICS.credit_id</code>.</td></tr>
    <tr><td><code>entry_price</code></td><td>NUMERIC(12,4)</td><td>NO</td><td>&mdash;</td><td>&mdash;</td><td>Recommended execution fill price.</td></tr>
    <tr><td><code>stop_loss_price</code></td><td>NUMERIC(12,4)</td><td>NO</td><td>&mdash;</td><td>&mdash;</td><td>Dynamic lower barrier: <math xmlns="http://www.w3.org/1998/Math/MathML" display="inline"><mrow><msub><mi>P</mi><mtext>entry</mtext></msub><mo>&#x02212;</mo><mn>1.5</mn><mo>&#x000B7;</mo><mtext>ATR</mtext></mrow></math>.</td></tr>
    <tr><td><code>take_profit_1</code></td><td>NUMERIC(12,4)</td><td>NO</td><td>&mdash;</td><td>&mdash;</td><td>Dynamic upper barrier 1: <math xmlns="http://www.w3.org/1998/Math/MathML" display="inline"><mrow><msub><mi>P</mi><mtext>entry</mtext></msub><mo>&#x0002B;</mo><mn>2.0</mn><mo>&#x000B7;</mo><mtext>ATR</mtext></mrow></math>.</td></tr>
    <tr><td><code>take_profit_2</code></td><td>NUMERIC(12,4)</td><td>NO</td><td>&mdash;</td><td>&mdash;</td><td>Dynamic upper barrier 2: <math xmlns="http://www.w3.org/1998/Math/MathML" display="inline"><mrow><msub><mi>P</mi><mtext>entry</mtext></msub><mo>&#x0002B;</mo><mn>3.5</mn><mo>&#x000B7;</mo><mtext>ATR</mtext></mrow></math>.</td></tr>
    <tr><td><code>kelly_fraction</code></td><td>NUMERIC(6,4)</td><td>NO</td><td>&mdash;</td><td>&mdash;</td><td>Optimal Half-Kelly allocation fraction <math xmlns="http://www.w3.org/1998/Math/MathML" display="inline"><mrow><msubsup><mi>f</mi><mtext>half</mtext><mo>&#x0002A;</mo></msubsup><mo>&#x02264;</mo><mn>0.20</mn></mrow></math>.</td></tr>
  </tbody>
</table>

<!-- Table 11: BacktestPortfolios -->
<h4>Table 11: <code>BACKTEST_PORTFOLIOS</code> (Portfolio Performance Summary)</h4>
<table>
  <thead>
    <tr><th>Column Name</th><th>Data Type</th><th>Null?</th><th>Key</th><th>Default</th><th>Description &amp; Business Constraints</th></tr>
  </thead>
  <tbody>
    <tr><td><code>portfolio_id</code></td><td>BIGINT</td><td>NO</td><td>PK</td><td>AUTO</td><td>Backtest simulation run identifier.</td></tr>
    <tr><td><code>run_id</code></td><td>BIGINT</td><td>NO</td><td>FK</td><td>&mdash;</td><td>References <code>MODEL_TRAINING_RUNS.run_id</code>.</td></tr>
    <tr><td><code>initial_capital</code></td><td>NUMERIC(14,2)</td><td>NO</td><td>&mdash;</td><td>100000.00</td><td>Starting equity capital ($).</td></tr>
    <tr><td><code>final_value</code></td><td>NUMERIC(14,2)</td><td>NO</td><td>&mdash;</td><td>&mdash;</td><td>Final cumulative portfolio equity ($).</td></tr>
    <tr><td><code>sharpe_ratio</code></td><td>NUMERIC(6,3)</td><td>NO</td><td>&mdash;</td><td>&mdash;</td><td>Annualized risk-adjusted excess return.</td></tr>
    <tr><td><code>max_drawdown_pct</code></td><td>NUMERIC(6,3)</td><td>NO</td><td>&mdash;</td><td>&mdash;</td><td>Peak-to-trough maximum drawdown %.</td></tr>
    <tr><td><code>win_rate_pct</code></td><td>NUMERIC(6,3)</td><td>NO</td><td>&mdash;</td><td>&mdash;</td><td>Percentage of closed trades with positive net PnL.</td></tr>
  </tbody>
</table>

<!-- Table 12: BacktestTrades -->
<h4>Table 12: <code>BACKTEST_TRADES</code> (Itemized Trade Execution Log)</h4>
<table>
  <thead>
    <tr><th>Column Name</th><th>Data Type</th><th>Null?</th><th>Key</th><th>Default</th><th>Description &amp; Business Constraints</th></tr>
  </thead>
  <tbody>
    <tr><td><code>trade_id</code></td><td>BIGINT</td><td>NO</td><td>PK</td><td>AUTO</td><td>Unique trade execution identifier.</td></tr>
    <tr><td><code>portfolio_id</code></td><td>BIGINT</td><td>NO</td><td>FK</td><td>&mdash;</td><td>References <code>BACKTEST_PORTFOLIOS.portfolio_id</code>.</td></tr>
    <tr><td><code>trade_direction</code></td><td>VARCHAR(8)</td><td>NO</td><td>&mdash;</td><td>'LONG'</td><td><code>'LONG'</code> or <code>'SHORT'</code>.</td></tr>
    <tr><td><code>fill_price</code></td><td>NUMERIC(12,4)</td><td>NO</td><td>&mdash;</td><td>&mdash;</td><td>Price at entry order fill including slippage.</td></tr>
    <tr><td><code>exit_price</code></td><td>NUMERIC(12,4)</td><td>NO</td><td>&mdash;</td><td>&mdash;</td><td>Price at trade exit fill.</td></tr>
    <tr><td><code>realized_pnl</code></td><td>NUMERIC(12,2)</td><td>NO</td><td>&mdash;</td><td>&mdash;</td><td>Net profit or loss in portfolio currency.</td></tr>
    <tr><td><code>exit_reason</code></td><td>VARCHAR(32)</td><td>NO</td><td>&mdash;</td><td>&mdash;</td><td><code>'TAKE_PROFIT'</code>, <code>'STOP_LOSS'</code>, <code>'TIME_EXPIRY'</code>.</td></tr>
  </tbody>
</table>

<h3>3.4 Indexing &amp; Query Optimization Strategy</h3>
<ul>
  <li><strong>Composite Index <code>idx_candle_ticker_time</code>:</strong> <code>CREATE UNIQUE INDEX idx_candle_ticker_time ON CANDLE_DATA_1D (ticker, timestamp_utc DESC)</code> &mdash; Enables instant <math xmlns="http://www.w3.org/1998/Math/MathML" display="inline"><mrow><mi>O</mi><mo stretchy="false">&#x00028;</mo><mo>log</mo><mi>N</mi><mo stretchy="false">&#x00029;</mo></mrow></math> sliding-window retrieval for sequence lookbacks.</li>
  <li><strong>Index <code>idx_features_candle</code>:</strong> <code>CREATE INDEX idx_features_candle ON FEATURE_MATRIX_26 (candle_id)</code> &mdash; Enables 1:1 join with zero full-table scans.</li>
  <li><strong>Index <code>idx_pred_run_candle</code>:</strong> <code>CREATE INDEX idx_pred_run_candle ON INFERENCE_PREDICTIONS (run_id, candle_id)</code> &mdash; Optimizes ensemble blending.</li>
</ul>
"""
    res = template
    res = res.replace("{svg_er}", svg_er)
    return res
