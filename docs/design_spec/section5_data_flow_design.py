"""
Section 5: Data Flow Design Module (DFD Level 0, 1, 2 + Data Dictionary)
"""
try:
    from . import svg_diagrams as svgs
except Exception:
    import svg_diagrams as svgs

def get_section5_html():
    svg_dfd0 = svgs.get_dfd_level_0_svg()
    svg_dfd1 = svgs.get_dfd_level_1_svg()
    svg_dfd2 = svgs.get_dfd_level_2_svg()

    template = """
<!-- SECTION 5: DATA FLOW DESIGN -->
<div class="page-break"></div>
<h2>Section 5: Data Flow Design (DFD Levels 0, 1, and 2)</h2>

<p>
Data Flow Diagrams (DFDs) trace the progressive transformation of raw external market data as it moves through network ingestion, mathematical filtering, deep neural processing, selective risk gating, and final trade sizing.
</p>

<!-- 5.1 DFD LEVEL 0: CONTEXT -->
<h3>5.1 DFD Level 0: System Context Diagram</h3>
<p>
The Level 0 Context Diagram defines the top-level operational boundary of AlphaTemporal, identifying the primary human and external system entities interacting with the platform.
</p>
<div class="diagram-container">
  {svg_dfd0}
</div>

<!-- 5.2 DFD LEVEL 1: SUBSYSTEM -->
<div class="page-break"></div>
<h3>5.2 DFD Level 1: Subsystem Functional Decomposition</h3>
<p>
The Level 1 DFD decomposes the central system into six sequential data processing nodes (Processes 1.0 through 6.0) linked by five persistent data stores (D1 through D5).
</p>
<div class="diagram-container">
  {svg_dfd1}
</div>

<!-- 5.3 DFD LEVEL 2: DETAILED -->
<div class="page-break"></div>
<h3>5.3 DFD Level 2: Deep Dive into Process 3.0 (Inference) &amp; 4.0 (Selective Gating)</h3>
<p>
The Level 2 DFD provides an atomic breakdown of the AI Ensemble Inference Engine (Processes 3.1&ndash;3.4) and Chow Selective Classification Gating (Processes 4.1&ndash;4.3).
</p>
<div class="diagram-container">
  {svg_dfd2}
</div>

<!-- 5.4 DATA DICTIONARY -->
<h3>5.4 Comprehensive Data Flow Dictionary</h3>
<table>
  <thead>
    <tr><th style="width: 20%;">Data Flow Identifier</th><th>Source Process / Entity</th><th>Destination Process / Store</th><th>Data Structure &amp; Payload Fields</th></tr>
  </thead>
  <tbody>
    <tr>
      <td><code>DF1: RawMarketFeed</code></td>
      <td>NSE Gateway / Binance</td>
      <td>Process 1.0 (Ingestion)</td>
      <td><code>timestamp</code>, <code>open</code>, <code>high</code>, <code>low</code>, <code>close</code>, <code>volume</code>, <code>bid_depth</code>, <code>ask_depth</code>.</td>
    </tr>
    <tr>
      <td><code>DF2: CleanOHLCV</code></td>
      <td>Process 1.0</td>
      <td>Store D1 (Raw Price Store)</td>
      <td>Monotonic DatetimeIndex, session-locked close cross prices, validated volume.</td>
    </tr>
    <tr>
      <td><code>DF3: FeatureVector</code></td>
      <td>Process 2.0 (Vectorization)</td>
      <td>Store D2 (Feature Matrix)</td>
      <td>26 float arrays: <code>HMA_9</code>, <code>SuperTrend</code>, <code>ADX_14</code>, <code>RSI_14</code>, <code>FracDiff_d</code>, etc.</td>
    </tr>
    <tr>
      <td><code>DF4: SequenceTensor</code></td>
      <td>Process 3.1 (Sequence Formatter)</td>
      <td>Process 3.2 / 3.3 (GPU Models)</td>
      <td>3D PyTorch CUDA Tensor of dimensions: <code>(Batch_Size, Seq_Len=20, Features=26)</code>.</td>
    </tr>
    <tr>
      <td><code>DF5: RawPosteriors</code></td>
      <td>Process 3.4 (Meta-Learner)</td>
      <td>Store D3 (Posteriors Store)</td>
      <td>Calibrated probability vector: <code>[P(Down), P(Up)]</code> where <math xmlns="http://www.w3.org/1998/Math/MathML" display="inline"><mrow><mo>&#x02211;</mo><msub><mi>P</mi><mi>i</mi></msub><mo>&#x0003D;</mo><mn>1.0</mn></mrow></math>.</td>
    </tr>
    <tr>
      <td><code>DF6: SelectiveDecision</code></td>
      <td>Process 4.3 (Error Bounder)</td>
      <td>Store D4 (Selected Trades)</td>
      <td><code>status: 'EXECUTED'|'ABSTAIN'</code>, <code>confidence</code>, <code>error_bound &le; 0.25</code>.</td>
    </tr>
    <tr>
      <td><code>DF7: CreditRiskVeto</code></td>
      <td>Process 5.0 (Credit Distress)</td>
      <td>Process 6.0 (Capital Allocation)</td>
      <td><code>altman_z</code>, <code>merton_dd</code>, <code>distress_zone</code>, <code>buy_veto: bool</code>.</td>
    </tr>
    <tr>
      <td><code>DF8: TradeActionPlan</code></td>
      <td>Process 6.0 (Half-Kelly)</td>
      <td>Store D5 / Web UI Client</td>
      <td><code>entry_price</code>, <code>stop_loss</code>, <code>take_profit_1</code>, <code>take_profit_2</code>, <code>kelly_fraction &le; 0.20</code>.</td>
    </tr>
  </tbody>
</table>
"""
    res = template
    res = res.replace("{svg_dfd0}", svg_dfd0)
    res = res.replace("{svg_dfd1}", svg_dfd1)
    res = res.replace("{svg_dfd2}", svg_dfd2)
    return res
