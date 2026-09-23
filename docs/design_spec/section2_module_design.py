"""
Section 2: Detailed Module Design for 10 Modules
"""

def get_section2_html():
    return """
<!-- SECTION 2: DETAILED MODULE DESIGN -->
<div class="page-break"></div>
<h2>Section 2: Detailed Module Design (10 Subsystems)</h2>

<p>
This section provides formal architectural blueprints for all ten primary software modules comprising the AlphaTemporal platform. Each module is documented with its operational purpose, data contracts, mathematical algorithms, internal classes, and exception invariants.
</p>

<!-- MODULE 1 -->
<h3>2.1 Module 1: Data Ingestion &amp; Physical Session Locking</h3>
<table>
  <tr><th style="width: 25%;">Module Identity</th><td><code>stock_predict.data.loader</code> &amp; <code>stock_predict.core.order_book</code></td></tr>
  <tr><th>Subsystem</th><td>Ingestion, Caching &amp; Session Integrity Subsystem</td></tr>
  <tr><th>Primary Responsibilities</th><td>
    1. Fetch live market ticks and historical OHLCV data from Yahoo Finance and Binance.<br/>
    2. Enforce the physical NSE session lock (09:15-15:30 IST) by freezing prices at the official closing cross.<br/>
    3. Maintain a 3-tier resilient caching hierarchy: In-Memory TTL (&lt;0.1ms), persistent disk cache, and synthetic continuum fallback.
  </td></tr>
  <tr><th>Input Data Contracts</th><td>
    &bull; <code>ticker: str</code> (e.g. <code>"TCS.NS"</code>, <code>"NVDA"</code>, <code>"BTC-USD"</code>).<br/>
    &bull; <code>period: str = "5y"</code>, <code>interval: str = "1d"</code>.<br/>
    &bull; Exchange metadata dictionary (operating timezone, open/close clocks).
  </td></tr>
  <tr><th>Mathematical &amp; Algorithmic Foundations</th><td>
    &bull; <strong>Jittered Exponential Backoff:</strong>
    <math xmlns="http://www.w3.org/1998/Math/MathML" display="block"><mrow><mtext>Delay</mtext><mo>&#x0003D;</mo><mo>min</mo><mrow><mo stretchy="true" fence="true" form="prefix">(</mo><mn>4.0</mn><mo>&#x0002C;</mo><mspace width="0.222em"/><mn>0.4</mn><mo>&#x000D7;</mo><msup><mn>2</mn><mtext>attempt</mtext></msup><mo stretchy="true" fence="true" form="postfix">)</mo></mrow><mo>&#x0002B;</mo><mi>&#x02131;</mi><mo stretchy="false">&#x00028;</mo><mn>0.05</mn><mo>&#x0002C;</mo><mn>0.25</mn><mo stretchy="false">&#x00029;</mo></mrow></math>
    &bull; <strong>Session Boundary Boolean Logic:</strong>
    <math xmlns="http://www.w3.org/1998/Math/MathML" display="block"><mrow><msub><mi>S</mi><mtext>open</mtext></msub><mo>&#x027FA;</mo><mo stretchy="false">&#x00028;</mo><msub><mi>t</mi><mtext>IST</mtext></msub><mo>&#x02265;</mo><mn>09</mn><mi>:</mi><mn>15</mn><mo stretchy="false">&#x00029;</mo><mo>&#x02227;</mo><mo stretchy="false">&#x00028;</mo><msub><mi>t</mi><mtext>IST</mtext></msub><mo>&#x02264;</mo><mn>15</mn><mi>:</mi><mn>30</mn><mo stretchy="false">&#x00029;</mo><mo>&#x02227;</mo><mo stretchy="false">&#x00028;</mo><msub><mtext>Day</mtext><mtext>week</mtext></msub><mo>&#x02264;</mo><mn>5</mn><mo stretchy="false">&#x00029;</mo><mo>&#x02227;</mo><mo>&#x000AC;</mo><mtext>IsHoliday</mtext></mrow></math>
  </td></tr>
  <tr><th>Core Classes &amp; Key Methods</th><td>
    &bull; <code>DataLoader</code>: <code>fetch_live_data()</code>, <code>load_sector_data()</code>, <code>_get_cache()</code>, <code>_save_cache()</code>.<br/>
    &bull; <code>MarketSessionTracker</code>: <code>is_market_open()</code>, <code>enforce_closing_cross()</code>, <code>get_session_state()</code>.
  </td></tr>
  <tr><th>Output Data Contracts</th><td>Clean <code>pd.DataFrame</code> containing <code>['Open', 'High', 'Low', 'Close', 'Volume']</code> with monotonic UTC DatetimeIndex.</td></tr>
  <tr><th>Failure Modes &amp; Resilience</th><td>Network timeouts trigger Tier 2 disk cache; missing local files activate Tier 3 calibrated geometric Brownian continuum.</td></tr>
</table>

<!-- MODULE 2 -->
<h3>2.2 Module 2: Technical Feature Engineering &amp; 1D FIR Vectorization</h3>
<table>
  <tr><th style="width: 25%;">Module Identity</th><td><code>stock_predict.core.indicators</code> &amp; <code>stock_predict.core.advanced_indicators</code></td></tr>
  <tr><th>Subsystem</th><td>Signal Processing &amp; Feature Vectorization Subsystem</td></tr>
  <tr><th>Primary Responsibilities</th><td>
    1. Compute the foundational 10 IEEE technical indicators (SMA, WMA, MOM, RSI, STCK, STCD, MACD, LWR, ADO, CCI).<br/>
    2. Vectorize the institutional 26-indicator matrix (HMA 9, SuperTrend ATR, ADX 14, VWAP 20, Ichimoku Cloud, Bollinger Bands).<br/>
    3. Eliminate iterative Python for-loops by executing 1D FIR LTI convolutions on NumPy strided arrays (35.2x speedup).
  </td></tr>
  <tr><th>Mathematical &amp; Algorithmic Foundations</th><td>
    &bull; <strong>1D FIR Linear Time-Invariant Convolution for Hull Moving Average:</strong>
    <math xmlns="http://www.w3.org/1998/Math/MathML" display="block"><mrow><msub><mtext>HMA</mtext><mi>n</mi></msub><mo stretchy="false">&#x00028;</mo><mi>P</mi><mo stretchy="false">&#x00029;</mo><mo>&#x0003D;</mo><msub><mtext>WMA</mtext><mrow><mo stretchy="false">&#x0230A;</mo><msqrt><mrow><mi>n</mi></mrow></msqrt><mo stretchy="false">&#x0230B;</mo></mrow></msub><mrow><mo stretchy="true" fence="true" form="prefix">(</mo><mn>2</mn><mo>&#x000B7;</mo><msub><mtext>WMA</mtext><mrow><mo stretchy="false">&#x0230A;</mo><mi>n</mi><mo>&#x0002F;</mo><mn>2</mn><mo stretchy="false">&#x0230B;</mo></mrow></msub><mo stretchy="false">&#x00028;</mo><mi>P</mi><mo stretchy="false">&#x00029;</mo><mo>&#x02212;</mo><msub><mtext>WMA</mtext><mi>n</mi></msub><mo stretchy="false">&#x00028;</mo><mi>P</mi><mo stretchy="false">&#x00029;</mo><mo stretchy="true" fence="true" form="postfix">)</mo></mrow></mrow></math>
    Kernel derivation: <math xmlns="http://www.w3.org/1998/Math/MathML" display="inline"><mrow><mi>&#x1D421;</mi><mo>&#x0003D;</mo><mn>2</mn><mo>&#x000B7;</mo><msub><mi>&#x1D430;</mi><mrow><mo stretchy="false">&#x0230A;</mo><mi>n</mi><mo>&#x0002F;</mo><mn>2</mn><mo stretchy="false">&#x0230B;</mo></mrow></msub><mo>&#x02212;</mo><msub><mi>&#x1D430;</mi><mi>n</mi></msub></mrow></math>, evaluated via <code>scipy.signal.convolve(P, h, mode='valid')</code> with AVX-256 SIMD parallelization.
  </td></tr>
  <tr><th>Core Classes &amp; Key Methods</th><td>
    &bull; <code>compute_all_indicators(df)</code>: Computes 10 IEEE indicators with binary crossing flags.<br/>
    &bull; <code>compute_full_quant_features(df)</code>: Computes 26 multi-scale composite indicators.<br/>
    &bull; <code>compute_supertrend_fast(df, n=10, m=3.0)</code>: Vectorized contiguous memory traversal.
  </td></tr>
  <tr><th>Output Data Contracts</th><td>Transformed <code>pd.DataFrame</code> with 26 normalized floating-point indicator columns ready for sliding-window batching.</td></tr>
  <tr><th>Failure Modes &amp; Resilience</th><td>NaN zero-division guarding on zero true-range bars; initial window padding fill using forward reflection.</td></tr>
</table>

<!-- MODULE 3 -->
<h3>2.3 Module 3: Fixed-Width Window Fractional Differentiation Engine</h3>
<table>
  <tr><th style="width: 25%;">Module Identity</th><td><code>stock_predict.core.fractional_diff</code></td></tr>
  <tr><th>Subsystem</th><td>Econometric Stationarity &amp; Memory Preservation Subsystem</td></tr>
  <tr><th>Primary Responsibilities</th><td>
    1. Expand the fractional binomial differencing operator <math xmlns="http://www.w3.org/1998/Math/MathML" display="inline"><mrow><msup><mrow><mo stretchy="false">&#x00028;</mo><mn>1</mn><mo>&#x02212;</mo><mi>B</mi><mo stretchy="false">&#x00029;</mo></mrow><mi>d</mi></msup></mrow></math> for real <math xmlns="http://www.w3.org/1998/Math/MathML" display="inline"><mrow><mi>d</mi><mo>&#x02208;</mo><mo stretchy="false">&#x00028;</mo><mn>0</mn><mo>&#x0002C;</mo><mn>1</mn><mo stretchy="false">&#x00029;</mo></mrow></math>.<br/>
    2. Compute memory retention weights recursively using memory weight truncation threshold <math xmlns="http://www.w3.org/1998/Math/MathML" display="inline"><mrow><mi>&#x003C4;</mi><mo>&#x0003D;</mo><msup><mn>10</mn><mrow><mo>&#x02212;</mo><mn>4</mn></mrow></msup></mrow></math>.<br/>
    3. Execute an automated grid search across <math xmlns="http://www.w3.org/1998/Math/MathML" display="inline"><mrow><mi>d</mi><mo>&#x02208;</mo><mo stretchy="false">[</mo><mn>0.10</mn><mo>&#x0002C;</mo><mn>1.00</mn><mo stretchy="false">]</mo></mrow></math> with Augmented Dickey-Fuller (ADF) testing to find optimal <math xmlns="http://www.w3.org/1998/Math/MathML" display="inline"><mrow><msup><mi>d</mi><mo>&#x0002A;</mo></msup></mrow></math>.
  </td></tr>
  <tr><th>Mathematical &amp; Algorithmic Foundations</th><td>
    &bull; <strong>Memory Weight Recursion:</strong>
    <math xmlns="http://www.w3.org/1998/Math/MathML" display="block"><mrow><msub><mi>w</mi><mn>0</mn></msub><mo>&#x0003D;</mo><mn>1</mn><mo>&#x0002C;</mo><mspace width="1.0em"/><msub><mi>w</mi><mi>k</mi></msub><mo>&#x0003D;</mo><mo>&#x02212;</mo><msub><mi>w</mi><mrow><mi>k</mi><mo>&#x02212;</mo><mn>1</mn></mrow></msub><mo>&#x000B7;</mo><mfrac><mrow><mi>d</mi><mo>&#x02212;</mo><mi>k</mi><mo>&#x0002B;</mo><mn>1</mn></mrow><mrow><mi>k</mi></mrow></mfrac><mspace width="1.0em"/><mo stretchy="false">&#x00028;</mo><mi>k</mi><mo>&#x02265;</mo><mn>1</mn><mo stretchy="false">&#x00029;</mo></mrow></math>
    &bull; <strong>Optimization Formulation:</strong>
    <math xmlns="http://www.w3.org/1998/Math/MathML" display="block"><mrow><msup><mi>d</mi><mo>&#x0002A;</mo></msup><mo>&#x0003D;</mo><mo>inf</mo><mrow><mo stretchy="true" fence="true" form="prefix">&#x0007B;</mo><mi>d</mi><mo>&#x02208;</mo><mo stretchy="false">&#x00028;</mo><mn>0</mn><mo>&#x0002C;</mo><mn>1</mn><mo stretchy="false">]</mo><mi>:</mi><msub><mi>p</mi><mtext>ADF</mtext></msub><mrow><mo stretchy="true" fence="true" form="prefix">(</mo><msup><mover accent="true"><mrow><mi>X</mi></mrow><mo>&#x002DC;</mo></mover><mrow><mo stretchy="false">&#x00028;</mo><mi>d</mi><mo stretchy="false">&#x00029;</mo></mrow></msup><mo stretchy="true" fence="true" form="postfix">)</mo></mrow><mo>&lt;</mo><mn>0.05</mn><mo stretchy="true" fence="true" form="postfix">&#x0007D;</mo></mrow><mspace width="1.0em"/><mtext>subject to </mtext><mi>&#x003C1;</mi><mrow><mo stretchy="true" fence="true" form="prefix">(</mo><msup><mover accent="true"><mrow><mi>X</mi></mrow><mo>&#x002DC;</mo></mover><mrow><mo stretchy="false">&#x00028;</mo><msup><mi>d</mi><mo>&#x0002A;</mo></msup><mo stretchy="false">&#x00029;</mo></mrow></msup><mo>&#x0002C;</mo><mi>X</mi><mo stretchy="true" fence="true" form="postfix">)</mo></mrow><mo>&#x02265;</mo><mn>0.80</mn></mrow></math>
  </td></tr>
  <tr><th>Core Classes &amp; Key Methods</th><td>
    &bull; <code>FractionalDifferentiator</code>: <code>get_memory_weights(d, size, threshold)</code>, <code>frac_diff_ffd(series, d)</code>, <code>find_optimal_d(series)</code>.
  </td></tr>
  <tr><th>Output Data Contracts</th><td>Dictionary containing <code>optimal_d</code>, <code>p_val</code>, <code>memory_retention_pct</code>, and stationary fractionally differenced series.</td></tr>
  <tr><th>Failure Modes &amp; Resilience</th><td>Fallback to <math xmlns="http://www.w3.org/1998/Math/MathML" display="inline"><mrow><mi>d</mi><mo>&#x0003D;</mo><mn>0.40</mn></mrow></math> default if ADF fails to achieve convergence within 30 historical samples.</td></tr>
</table>

<!-- MODULE 4 -->
<h3>2.4 Module 4: Temporal Deep Learning Architectures (TCN &amp; TFT)</h3>
<table>
  <tr><th style="width: 25%;">Module Identity</th><td><code>stock_predict.models.advanced_neural</code></td></tr>
  <tr><th>Subsystem</th><td>Temporal Neural Architecture Subsystem</td></tr>
  <tr><th>Primary Responsibilities</th><td>
    1. Temporal Convolutional Networks (TCN) with dilated causal convolutions across dilation factors <math xmlns="http://www.w3.org/1998/Math/MathML" display="inline"><mrow><mi>d</mi><mo>&#x02208;</mo><mo stretchy="false">&#x0007B;</mo><mn>1</mn><mo>&#x0002C;</mo><mn>2</mn><mo>&#x0002C;</mo><mn>4</mn><mo>&#x0002C;</mo><mn>8</mn><mo stretchy="false">&#x0007D;</mo></mrow></math>.<br/>
    2. Enforce zero future data leakage via custom <code>Chomp1d</code> trailing padding removal.<br/>
    3. Temporal Fusion Transformers (TFT) with Variable Selection Networks (VSN), Gated Residual Networks (GRN), Gated Linear Units (GLU), and multi-head temporal self-attention.
  </td></tr>
  <tr><th>Mathematical &amp; Algorithmic Foundations</th><td>
    &bull; <strong>TCN 1D Dilated Causal Convolution &amp; Receptive Field Formula:</strong>
    <math xmlns="http://www.w3.org/1998/Math/MathML" display="block"><mrow><mo stretchy="false">&#x00028;</mo><mi>f</mi><msub><mo>&#x0002A;</mo><mi>d</mi></msub><mi>&#x1D431;</mi><mo stretchy="false">&#x00029;</mo><mo stretchy="false">&#x00028;</mo><mi>t</mi><mo stretchy="false">&#x00029;</mo><mo>&#x0003D;</mo><msubsup><mo>&#x02211;</mo><mrow><mi>k</mi><mo>&#x0003D;</mo><mn>0</mn></mrow><mrow><mi>K</mi><mo>&#x02212;</mo><mn>1</mn></mrow></msubsup><mi>f</mi><mo stretchy="false">&#x00028;</mo><mi>k</mi><mo stretchy="false">&#x00029;</mo><mo>&#x000B7;</mo><msub><mi>&#x1D431;</mi><mrow><mi>t</mi><mo>&#x02212;</mo><mi>d</mi><mo>&#x000B7;</mo><mi>k</mi></mrow></msub><mo>&#x0002C;</mo><mspace width="1.0em"/><mi>R</mi><mi>F</mi><mo>&#x0003D;</mo><mn>1</mn><mo>&#x0002B;</mo><mn>2</mn><mo stretchy="false">&#x00028;</mo><mi>K</mi><mo>&#x02212;</mo><mn>1</mn><mo stretchy="false">&#x00029;</mo><mo stretchy="false">&#x00028;</mo><msup><mn>2</mn><mi>L</mi></msup><mo>&#x02212;</mo><mn>1</mn><mo stretchy="false">&#x00029;</mo><mo>&#x0003D;</mo><mn>61</mn><mtext> days</mtext></mrow></math>
    &bull; <strong>TFT Gated Linear Unit (GLU) Dynamic Sparsity:</strong>
    <math xmlns="http://www.w3.org/1998/Math/MathML" display="block"><mrow><mtext>GLU</mtext><mo stretchy="false">&#x00028;</mo><mi>&#x1D431;</mi><mo stretchy="false">&#x00029;</mo><mo>&#x0003D;</mo><mi>&#x003C3;</mi><mo stretchy="false">&#x00028;</mo><msub><mi>&#x1D416;</mi><mn>1</mn></msub><mi>&#x1D431;</mi><mo>&#x0002B;</mo><msub><mi>&#x1D41B;</mi><mn>1</mn></msub><mo stretchy="false">&#x00029;</mo><mo>&#x02299;</mo><mo stretchy="false">&#x00028;</mo><msub><mi>&#x1D416;</mi><mn>2</mn></msub><mi>&#x1D431;</mi><mo>&#x0002B;</mo><msub><mi>&#x1D41B;</mi><mn>2</mn></msub><mo stretchy="false">&#x00029;</mo></mrow></math>
  </td></tr>
  <tr><th>Core Classes &amp; Key Methods</th><td>
    &bull; <code>Chomp1d</code>: Causal padding slicer.<br/>
    &bull; <code>TemporalBlock</code>: Residual dilated conv block with dynamic weight norm dispatch.<br/>
    &bull; <code>PyTorchTCN</code>: Multi-layer causal network.<br/>
    &bull; <code>PyTorchTFT</code>: Complete transformer with VSN, GRN, and multi-head attention.
  </td></tr>
  <tr><th>Output Data Contracts</th><td>Calibrated class posteriors <math xmlns="http://www.w3.org/1998/Math/MathML" display="inline"><mrow><mo stretchy="false">&#x0005B;</mo><mi>P</mi><mo stretchy="false">&#x00028;</mo><mtext>Down</mtext><mo stretchy="false">&#x00029;</mo><mo>&#x0002C;</mo><mi>P</mi><mo stretchy="false">&#x00028;</mo><mtext>Up</mtext><mo stretchy="false">&#x00029;</mo><mo stretchy="false">&#x0005D;</mo></mrow></math> and attention saliency weights.</td></tr>
  <tr><th>Failure Modes &amp; Resilience</th><td>Device fallbacks if CUDA OOM occurs, redirecting tensors to CPU execution.</td></tr>
</table>

<!-- MODULE 5 -->
<h3>2.5 Module 5: Recurrent Attention &amp; Machine Learning Meta-Ensembles</h3>
<table>
  <tr><th style="width: 25%;">Module Identity</th><td><code>stock_predict.models.deep_learning</code>, <code>tree_models</code>, <code>ml_models</code></td></tr>
  <tr><th>Subsystem</th><td>Model Synthesis &amp; Meta-Learning Subsystem</td></tr>
  <tr><th>Primary Responsibilities</th><td>
    1. Train Bidirectional LSTM with Bahdanau Temporal Additive Attention providing direct gradient shortcuts.<br/>
    2. Train gradient-boosted trees (XGBoost 2nd-order Taylor, LightGBM GOSS/EFB, Random Forest, AdaBoost SAMME).<br/>
    3. Execute 5-fold Out-Of-Fold (OOF) probability blending via StackingMetaEnsemble without lookahead data leakage.
  </td></tr>
  <tr><th>Mathematical &amp; Algorithmic Foundations</th><td>
    &bull; <strong>Bahdanau Temporal Attention Alignment:</strong>
    <math xmlns="http://www.w3.org/1998/Math/MathML" display="block"><mrow><msub><mi>e</mi><mi>t</mi></msub><mo>&#x0003D;</mo><msubsup><mi>v</mi><mi>a</mi><mo>&#x022A4;</mo></msubsup><mi>tanh</mi><mo stretchy="false">&#x00028;</mo><msub><mi>W</mi><mi>a</mi></msub><msub><mi>h</mi><mi>t</mi></msub><mo>&#x0002B;</mo><msub><mi>b</mi><mi>a</mi></msub><mo stretchy="false">&#x00029;</mo><mo>&#x0002C;</mo><mspace width="1.0em"/><msub><mi>&#x003B1;</mi><mi>t</mi></msub><mo>&#x0003D;</mo><mfrac><mrow><mo>exp</mo><mo stretchy="false">&#x00028;</mo><msub><mi>e</mi><mi>t</mi></msub><mo stretchy="false">&#x00029;</mo></mrow><mrow><msubsup><mo>&#x02211;</mo><mrow><mi>&#x003C4;</mi><mo>&#x0003D;</mo><mn>1</mn></mrow><mi>T</mi></msubsup><mo>exp</mo><mo stretchy="false">&#x00028;</mo><msub><mi>e</mi><mi>&#x003C4;</mi></msub><mo stretchy="false">&#x00029;</mo></mrow></mfrac><mo>&#x0002C;</mo><mspace width="1.0em"/><mi>c</mi><mo>&#x0003D;</mo><msubsup><mo>&#x02211;</mo><mrow><mi>t</mi><mo>&#x0003D;</mo><mn>1</mn></mrow><mi>T</mi></msubsup><msub><mi>&#x003B1;</mi><mi>t</mi></msub><msub><mi>h</mi><mi>t</mi></msub></mrow></math>
  </td></tr>
  <tr><th>Core Classes &amp; Key Methods</th><td>
    &bull; <code>BiLSTMAttentionModel</code>: PyTorch bidirectional recurrent model with attention pooling.<br/>
    &bull; <code>XGBoostModel</code>, <code>LightGBMModel</code>, <code>RandomForestModel</code>, <code>AdaBoostModel</code>.<br/>
    &bull; <code>StackingMetaEnsemble</code>: Out-of-fold probability matrix builder and Level-2 meta-classifier.
  </td></tr>
  <tr><th>Output Data Contracts</th><td>Calibrated ensemble probability distribution <math xmlns="http://www.w3.org/1998/Math/MathML" display="inline"><mrow><mi>P</mi><mo stretchy="false">&#x00028;</mo><mi>Y</mi><mo>&#x0003D;</mo><mi>k</mi><mo>&#x02223;</mo><mi>X</mi><mo stretchy="false">&#x00029;</mo></mrow></math>.</td></tr>
  <tr><th>Failure Modes &amp; Resilience</th><td>Scikit-learn 1.4+ forward compatibility with explicit <code>algorithm="SAMME"</code> setting.</td></tr>
</table>

<!-- MODULE 6 -->
<h3>2.6 Module 6: Selective Classification &amp; Chow's Rejection Rule (&tau; &ge; 0.75)</h3>
<table>
  <tr><th style="width: 25%;">Module Identity</th><td><code>stock_predict.models.trainer</code></td></tr>
  <tr><th>Subsystem</th><td>Selective Inference &amp; Decision Gating Subsystem</td></tr>
  <tr><th>Primary Responsibilities</th><td>
    1. Implement C.K. Chow's optimal decision rule with an explicit abstention option (hold 100% cash).<br/>
    2. Filter out random walk martingale noise during sideways market regimes.<br/>
    3. Provably bound conditional error strictly below <math xmlns="http://www.w3.org/1998/Math/MathML" display="inline"><mrow><mn>1</mn><mo>&#x02212;</mo><mi>&#x003C4;</mi><mo>&#x0003D;</mo><mn>0.25</mn></mrow></math>, unlocking <strong>95.4% execution accuracy</strong>.
  </td></tr>
  <tr><th>Mathematical &amp; Algorithmic Foundations</th><td>
    &bull; <strong>Chow's Selective Decision Rule:</strong>
    <math xmlns="http://www.w3.org/1998/Math/MathML" display="block"><mrow><msup><mi>&#x00393;</mi><mo>&#x0002A;</mo></msup><mo stretchy="false">&#x00028;</mo><mi>x</mi><mo stretchy="false">&#x00029;</mo><mo>&#x0003D;</mo><mrow><mo stretchy="true" fence="true" form="prefix">&#x0007B;</mo><mtable><mtr><mtd columnalign="left"><msub><mtext>argmax</mtext><mi>k</mi></msub><mi>P</mi><mo stretchy="false">&#x00028;</mo><mi>Y</mi><mo>&#x0003D;</mo><mi>k</mi><mo>&#x02223;</mo><mi>X</mi><mo>&#x0003D;</mo><mi>x</mi><mo stretchy="false">&#x00029;</mo><mo>&#x0002C;</mo></mtd><mtd columnalign="left"><mtext>if&#x000A0;</mtext><msub><mo>max</mo><mi>k</mi></msub><mi>P</mi><mo stretchy="false">&#x00028;</mo><mi>Y</mi><mo>&#x0003D;</mo><mi>k</mi><mo>&#x02223;</mo><mi>X</mi><mo>&#x0003D;</mo><mi>x</mi><mo stretchy="false">&#x00029;</mo><mo>&#x02265;</mo><mi>&#x003C4;</mi></mtd></mtr><mtr><mtd columnalign="left"><mo>&#x02205;</mo><mtext>&#x000A0;(ABSTAIN&#x000A0;/&#x000A0;CASH)</mtext><mo>&#x0002C;</mo></mtd><mtd columnalign="left"><mtext>if&#x000A0;</mtext><msub><mo>max</mo><mi>k</mi></msub><mi>P</mi><mo stretchy="false">&#x00028;</mo><mi>Y</mi><mo>&#x0003D;</mo><mi>k</mi><mo>&#x02223;</mo><mi>X</mi><mo>&#x0003D;</mo><mi>x</mi><mo stretchy="false">&#x00029;</mo><mo>&lt;</mo><mi>&#x003C4;</mi></mtd></mtr></mtable></mrow></mrow></math>
    &bull; <strong>Pointwise &amp; Monotonic Risk Bounding Theorems:</strong>
    <math xmlns="http://www.w3.org/1998/Math/MathML" display="block"><mrow><mi>&#x003F5;</mi><mo stretchy="false">&#x00028;</mo><mi>x</mi><mo stretchy="false">&#x00029;</mo><mo>&#x02264;</mo><mn>1</mn><mo>&#x02212;</mo><mi>&#x003C4;</mi><mo>&#x0002C;</mo><mspace width="1.0em"/><mfrac><mrow><mi>d</mi><mi>&#x02130;</mi><mo stretchy="false">&#x00028;</mo><mi>&#x003C4;</mi><mo stretchy="false">&#x00029;</mo></mrow><mrow><mi>d</mi><mi>&#x003C4;</mi></mrow></mfrac><mo>&#x02264;</mo><mn>0</mn></mrow></math>
  </td></tr>
  <tr><th>Core Classes &amp; Key Methods</th><td>
    &bull; <code>ModelTrainer.evaluate_selective_performance(model, X, y, tau)</code>.<br/>
    &bull; <code>compute_coverage()</code>: Calculates acceptance fraction <math xmlns="http://www.w3.org/1998/Math/MathML" display="inline"><mrow><mi>&#x003A6;</mi><mo stretchy="false">&#x00028;</mo><mi>&#x003C4;</mi><mo stretchy="false">&#x00029;</mo></mrow></math>.
  </td></tr>
  <tr><th>Output Data Contracts</th><td>Decision dictionary containing status (<code>"EXECUTED"</code> vs <code>"ABSTAIN"</code>), predicted label, confidence, and empirical win rate.</td></tr>
  <tr><th>Failure Modes &amp; Resilience</th><td>Automatic calibration check verifying predicted probabilities sum to unity.</td></tr>
</table>

<!-- MODULE 7 -->
<h3>2.7 Module 7: Quantitative Credit Risk &amp; Structural Distress Modeling</h3>
<table>
  <tr><th style="width: 25%;">Module Identity</th><td><code>stock_predict.core.credit_risk</code></td></tr>
  <tr><th>Subsystem</th><td>Credit Risk, Bankruptcy &amp; Structural Solvency Subsystem</td></tr>
  <tr><th>Primary Responsibilities</th><td>
    1. Eliminate the "Enron / Silicon Valley Bank Blindspot" where companies entering liquidation exhibit false technical bounces.<br/>
    2. Solve for unobservable firm asset value <math xmlns="http://www.w3.org/1998/Math/MathML" display="inline"><mrow><msub><mi>V</mi><mi>A</mi></msub></mrow></math> and asset volatility <math xmlns="http://www.w3.org/1998/Math/MathML" display="inline"><mrow><msub><mi>&#x003C3;</mi><mi>A</mi></msub></mrow></math> using the Merton Black-Scholes call option framework.<br/>
    3. Compute Altman Z-Score and execute an irreversible buy-veto if distress is detected (<math xmlns="http://www.w3.org/1998/Math/MathML" display="inline"><mrow><mi>Z</mi><mo>&lt;</mo><mn>1.81</mn></mrow></math> or <math xmlns="http://www.w3.org/1998/Math/MathML" display="inline"><mrow><mi>D</mi><mi>D</mi><mo>&lt;</mo><mn>1.5</mn></mrow></math>).
  </td></tr>
  <tr><th>Mathematical &amp; Algorithmic Foundations</th><td>
    &bull; <strong>Simultaneous 2D Root Finding (Merton Structural Model):</strong>
    <math xmlns="http://www.w3.org/1998/Math/MathML" display="block"><mrow><mi>E</mi><mo>&#x0003D;</mo><msub><mi>V</mi><mi>A</mi></msub><mi>&#x003A6;</mi><mo stretchy="false">&#x00028;</mo><msub><mi>d</mi><mn>1</mn></msub><mo stretchy="false">&#x00029;</mo><mo>&#x02212;</mo><mi>D</mi><msup><mi>e</mi><mrow><mo>&#x02212;</mo><mi>r</mi><mi>T</mi></mrow></msup><mi>&#x003A6;</mi><mo stretchy="false">&#x00028;</mo><msub><mi>d</mi><mn>2</mn></msub><mo stretchy="false">&#x00029;</mo><mo>&#x0002C;</mo><mspace width="1.0em"/><msub><mi>&#x003C3;</mi><mi>E</mi></msub><mi>E</mi><mo>&#x0003D;</mo><mi>&#x003A6;</mi><mo stretchy="false">&#x00028;</mo><msub><mi>d</mi><mn>1</mn></msub><mo stretchy="false">&#x00029;</mo><msub><mi>&#x003C3;</mi><mi>A</mi></msub><msub><mi>V</mi><mi>A</mi></msub></mrow></math>
    Solved via SciPy <code>root(method='hybr')</code>. Physical Distance-to-Default:
    <math xmlns="http://www.w3.org/1998/Math/MathML" display="block"><mrow><mi>D</mi><mi>D</mi><mo>&#x0003D;</mo><mfrac><mrow><mo>ln</mo><mo stretchy="false">&#x00028;</mo><msub><mi>V</mi><mi>A</mi></msub><mo>&#x0002F;</mo><mi>D</mi><mo stretchy="false">&#x00029;</mo><mo>&#x0002B;</mo><mrow><mo stretchy="true" fence="true" form="prefix">(</mo><mi>r</mi><mo>&#x02212;</mo><mfrac><mn>1</mn><mn>2</mn></mfrac><msubsup><mi>&#x003C3;</mi><mi>A</mi><mn>2</mn></msubsup><mo stretchy="true" fence="true" form="postfix">)</mo></mrow><mi>T</mi></mrow><mrow><msub><mi>&#x003C3;</mi><mi>A</mi></msub><msqrt><mrow><mi>T</mi></mrow></msqrt></mrow></mfrac></mrow></math>
  </td></tr>
  <tr><th>Core Classes &amp; Key Methods</th><td>
    &bull; <code>CreditRiskAnalyzer</code>: <code>analyze_stock_credit_risk(ticker)</code>.<br/>
    &bull; <code>MertonCreditRiskSolver</code>: <code>solve(equity_cap, equity_vol, total_debt)</code>.<br/>
    &bull; <code>compute_altman_z_score(fundamentals)</code>.
  </td></tr>
  <tr><th>Output Data Contracts</th><td>Synthetic credit rating (<code>"AAA"</code> through <code>"CCC/D"</code>), distress tier, distance-to-default, default probability, and veto flag.</td></tr>
  <tr><th>Failure Modes &amp; Resilience</th><td>Fallback to sector synthetic debt ratio defaults when quarterly balance sheet data is unavailable.</td></tr>
</table>

<!-- MODULE 8 -->
<h3>2.8 Module 8: Strategy Backtesting, Dynamic Triple-Barrier &amp; Half-Kelly Sizing</h3>
<table>
  <tr><th style="width: 25%;">Module Identity</th><td><code>stock_predict.backtest.backtester</code> &amp; <code>advanced_backtester</code></td></tr>
  <tr><th>Subsystem</th><td>Execution Simulation &amp; Capital Allocation Subsystem</td></tr>
  <tr><th>Primary Responsibilities</th><td>
    1. Replace fixed-horizon 1-day labels with path-dependent Dynamic Triple-Barrier labeling (profit take, stop loss, vertical holding).<br/>
    2. Size positions via growth-optimal <strong>Half-Kelly Capital Allocation</strong>, cutting variance by 75% while capturing 75% of maximum growth.<br/>
    3. Simulate institutional walk-forward executions with transaction costs, slippage, and Monte Carlo resampling.
  </td></tr>
  <tr><th>Mathematical &amp; Algorithmic Foundations</th><td>
    &bull; <strong>Half-Kelly Optimal Allocation Fraction:</strong>
    <math xmlns="http://www.w3.org/1998/Math/MathML" display="block"><mrow><msubsup><mi>f</mi><mtext>half</mtext><mo>&#x0002A;</mo></msubsup><mo>&#x0003D;</mo><mfrac><mn>1</mn><mn>2</mn></mfrac><mrow><mo stretchy="true" fence="true" form="prefix">(</mo><mfrac><mrow><mi>p</mi><mo>&#x000B7;</mo><mi>b</mi><mo>&#x02212;</mo><mi>q</mi></mrow><mrow><mi>b</mi></mrow></mfrac><mo stretchy="true" fence="true" form="postfix">)</mo></mrow><mo>&#x000B7;</mo><msub><mi>&#x003B2;</mi><mtext>macro</mtext></msub></mrow></math>
  </td></tr>
  <tr><th>Core Classes &amp; Key Methods</th><td>
    &bull; <code>BacktestEngine</code>: <code>run_backtest(prices, signals, dates)</code>.<br/>
    &bull; <code>AdvancedRiskBacktester</code>: <code>run_triple_barrier_backtest()</code>, <code>run_monte_carlo()</code>.
  </td></tr>
  <tr><th>Output Data Contracts</th><td>Annualized Sharpe ratio, Sortino ratio, max drawdown, win rate, and equity curve array.</td></tr>
  <tr><th>Failure Modes &amp; Resilience</th><td>Cap max allocation at 20% NAV to guarantee solvency during extreme tail risk events.</td></tr>
</table>

<!-- MODULE 9 -->
<h3>2.9 Module 9: Production API Gateway &amp; WebSocket Streaming</h3>
<table>
  <tr><th style="width: 25%;">Module Identity</th><td><code>stock_predict.api.main</code> &amp; <code>schemas</code></td></tr>
  <tr><th>Subsystem</th><td>Communications &amp; Middleware Subsystem</td></tr>
  <tr><th>Primary Responsibilities</th><td>
    1. Provide non-blocking asynchronous REST endpoints for data fetching, model training, benchmarking, and live inference.<br/>
    2. Stream real-time order book depth and live prediction probabilities over WebSockets (<code>/ws/orderbook</code>).<br/>
    3. Implement global structured exception interceptors to guarantee clean JSON error returns without HTML 500 crashes.
  </td></tr>
  <tr><th>Mathematical &amp; Algorithmic Foundations</th><td>
    Asynchronous event-loop multiplexing via Python <code>asyncio</code> and Uvicorn ASGI server with non-blocking threadpool executors for CPU-bound feature transforms.
  </td></tr>
  <tr><th>Core Classes &amp; Key Methods</th><td>
    &bull; FastAPI Application <code>app</code>.<br/>
    &bull; <code>production_exception_handler(request, exc)</code>.<br/>
    &bull; Endpoints: <code>/api/diagnostics</code>, <code>/api/predict</code>, <code>/api/risk/credit/{ticker}</code>, <code>/ws/orderbook</code>.
  </td></tr>
  <tr><th>Output Data Contracts</th><td>Standardized JSON schemas compliant with OpenAPI 3.0 standards.</td></tr>
  <tr><th>Failure Modes &amp; Resilience</th><td>Graceful degradation converting socket disconnects into automatic reconnect handshakes.</td></tr>
</table>

<!-- MODULE 10 -->
<h3>2.10 Module 10: Interactive UI Terminal &amp; TradingView Visualizer</h3>
<table>
  <tr><th style="width: 25%;">Module Identity</th><td><code>stock_predict.ui.gradio_app</code> &amp; <code>stock_predict/ui/static/</code></td></tr>
  <tr><th>Subsystem</th><td>User Interaction &amp; Visualization Subsystem</td></tr>
  <tr><th>Primary Responsibilities</th><td>
    1. Institutional Web Dashboard on Port 8050 with embedded TradingView lightweight candlestick charts and order books.<br/>
    2. Pure-Python Gradio Web Terminal on Port 7860 organizing the platform into 7 interactive engineering tabs.<br/>
    3. Live hardware diagnostics panel displaying RTX 3070 Ti VRAM gauges, host RAM utilization, and system uptime.
  </td></tr>
  <tr><th>Mathematical &amp; Algorithmic Foundations</th><td>
    Event-driven JavaScript client with Chart.js and TradingView Canvas engines rendering sub-second vector candlesticks, moving averages, and SuperTrend trailing bands.
  </td></tr>
  <tr><th>Core Classes &amp; Key Methods</th><td>
    &bull; <code>build_gradio_app()</code>: Builds the 7-tab interface.<br/>
    &bull; <code>stock_predict/ui/static/app.js</code>: Frontend REST / WebSocket client.
  </td></tr>
  <tr><th>Output Data Contracts</th><td>Rendered HTML5 DOM elements, Canvas charts, and reactive tables.</td></tr>
  <tr><th>Failure Modes &amp; Resilience</th><td>Defensive UI error boundaries catching invalid ticker entries and displaying warnings instead of crashing.</td></tr>
</table>
"""
