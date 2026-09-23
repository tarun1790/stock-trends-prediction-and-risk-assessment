"""
Section 4: UML Diagrams Module (All 8 Required Diagrams)
"""
try:
    from . import svg_diagrams as svgs
except Exception:
    import svg_diagrams as svgs

def get_section4_html():
    svg_uc = svgs.get_uml_use_case_svg()
    svg_cls = svgs.get_uml_class_svg()
    svg_seq = svgs.get_uml_sequence_svg()
    svg_col = svgs.get_uml_collaboration_svg()
    svg_act = svgs.get_uml_activity_svg()
    svg_comp = svgs.get_uml_component_svg()
    svg_dep = svgs.get_uml_deployment_svg()
    svg_state = svgs.get_uml_statechart_svg()

    template = """
<!-- SECTION 4: FORMAL UML DIAGRAMS -->
<div class="page-break"></div>
<h2>Section 4: Formal UML Diagram Catalog (UML 2.5 Standards)</h2>

<p>
This section presents the complete suite of eight formal Unified Modeling Language (UML 2.5) diagrams specifying the functional, static structural, dynamic behavioral, and physical deployment views of the AlphaTemporal platform.
</p>

<!-- 4.1 USE CASE DIAGRAM -->
<h3>4.1 UML Use Case Diagram</h3>
<p>
The Use Case Diagram defines the behavioral interactions between human/external system actors and the core capabilities encapsulated within the AlphaTemporal system boundary.
</p>
<div class="diagram-container">
  {svg_uc}
</div>

<h4>Use Case Specification &amp; Relationship Matrix</h4>
<table>
  <thead>
    <tr><th>Use Case ID</th><th>Use Case Title</th><th>Primary Actor</th><th>Stereotype / Relation</th><th>Operational Preconditions &amp; Flow</th></tr>
  </thead>
  <tbody>
    <tr><td><code>UC1</code></td><td>Ingest Live &amp; Historical Feeds</td><td>Trader / NSE / Binance</td><td>Primary</td><td>Asset symbol must exist in <code>EQUITIES</code>; streams real-time or historical OHLCV.</td></tr>
    <tr><td><code>UC2</code></td><td>Lock NSE Session Cross</td><td>NSE Gateway</td><td><code>&lt;&lt;include&gt;&gt;</code> UC1</td><td>Outside 09:15-15:30 IST, freezes prices at official closing cross cross with zero delta.</td></tr>
    <tr><td><code>UC3</code></td><td>Vectorize 26 Features &amp; HMA</td><td>Quantitative Trader</td><td>Primary</td><td>Invokes 1D FIR LTI convolution kernels across historical price windows.</td></tr>
    <tr><td><code>UC4</code></td><td>Fractional Diff Stationarity</td><td>System Automator</td><td><code>&lt;&lt;include&gt;&gt;</code> UC3</td><td>Computes optimal order <math xmlns="http://www.w3.org/1998/Math/MathML" display="inline"><mrow><msup><mi>d</mi><mo>&#x0002A;</mo></msup></mrow></math> guaranteeing ADF <math xmlns="http://www.w3.org/1998/Math/MathML" display="inline"><mrow><mi>p</mi><mo>&lt;</mo><mn>0.05</mn></mrow></math> while keeping memory &ge; 80%.</td></tr>
    <tr><td><code>UC5</code></td><td>Infer via TFT / TCN Ensemble</td><td>Quantitative Trader</td><td>Primary</td><td>Executes forward pass across 15+ models on the NVIDIA RTX 3070 Ti GPU.</td></tr>
    <tr><td><code>UC6</code></td><td>Abstain / Execute (Chow Rule)</td><td>Trader / Risk Manager</td><td><code>&lt;&lt;extend&gt;&gt;</code> UC5</td><td>Filters low-conviction predictions (<math xmlns="http://www.w3.org/1998/Math/MathML" display="inline"><mrow><mi>&#x003C4;</mi><mo>&lt;</mo><mn>0.75</mn></mrow></math>); forces 100% cash hold during sideways chop.</td></tr>
    <tr><td><code>UC7</code></td><td>Evaluate Merton &amp; Altman Veto</td><td>Risk Manager</td><td><code>&lt;&lt;include&gt;&gt;</code> UC6</td><td>Evaluates distance-to-default and Z-Score; halts execution if credit distress is flagged.</td></tr>
    <tr><td><code>UC8</code></td><td>Size Position via Half-Kelly</td><td>Trader / Portfolio Mgr</td><td><code>&lt;&lt;include&gt;&gt;</code> UC7</td><td>Calculates growth-optimal allocation fraction <math xmlns="http://www.w3.org/1998/Math/MathML" display="inline"><mrow><msubsup><mi>f</mi><mtext>half</mtext><mo>&#x0002A;</mo></msubsup></mrow></math> and dynamic triple barriers.</td></tr>
    <tr><td><code>UC9</code></td><td>Query CUDA RTX 3070 Ti Telemetry</td><td>System Administrator</td><td>Primary</td><td>Queries VRAM allocated/reserved, host RAM, CPU threads, and active cache counts.</td></tr>
  </tbody>
</table>

<!-- 4.2 CLASS DIAGRAM -->
<div class="page-break"></div>
<h3>4.2 UML Class Diagram (Static Structural View)</h3>
<p>
The Class Diagram details the object-oriented structure of the platform, including attributes, visibility modifiers (<code>+</code> public, <code>-</code> private, <code>#</code> protected), methods, inheritance relationships, and class associations.
</p>
<div class="diagram-container">
  {svg_cls}
</div>

<!-- 4.3 SEQUENCE DIAGRAM -->
<div class="page-break"></div>
<h3>4.3 UML Sequence Diagram (Dynamic Execution Trace)</h3>
<p>
The Sequence Diagram documents the chronological message dispatch sequence for an end-to-end institutional prediction query, illustrating synchronous calls, asynchronous worker transfers, return callbacks, and <code>alt</code> decision frames.
</p>
<div class="diagram-container">
  {svg_seq}
</div>

<!-- 4.4 COLLABORATION DIAGRAM -->
<div class="page-break"></div>
<h3>4.4 UML Collaboration / Communication Diagram</h3>
<p>
The Collaboration Diagram depicts the structural topology of interacting runtime objects and emphasizes message flow paths via decimal-numbered sequence chains.
</p>
<div class="diagram-container">
  {svg_col}
</div>

<!-- 4.5 ACTIVITY DIAGRAM -->
<div class="page-break"></div>
<h3>4.5 UML Activity Diagram (Algorithmic Control Flow)</h3>
<p>
The Activity Diagram illustrates the step-by-step workflow of signal generation, incorporating parallel execution forks (concurrent feature extraction and credit distress evaluation), join synchronization, and conditional decision branches.
</p>
<div class="diagram-container">
  {svg_act}
</div>

<!-- 4.6 COMPONENT DIAGRAM -->
<div class="page-break"></div>
<h3>4.6 UML Component Diagram (Software Packaging)</h3>
<p>
The Component Diagram details the modular decomposition of the codebase into reusable, encapsulated subsystems linked by provided and required service interfaces.
</p>
<div class="diagram-container">
  {svg_comp}
</div>

<!-- 4.7 DEPLOYMENT DIAGRAM -->
<div class="page-break"></div>
<h3>4.7 UML Deployment Diagram (Physical Execution Nodes)</h3>
<p>
The Deployment Diagram models the physical and virtual hardware environment, mapping software artifacts to execution environments, GPUs, filesystems, and external cloud gateways.
</p>
<div class="diagram-container">
  {svg_dep}
</div>

<!-- 4.8 STATE-CHART DIAGRAM -->
<div class="page-break"></div>
<h3>4.8 UML State-Chart Diagram (Signal Lifecycle State Machine)</h3>
<p>
The State-Chart Diagram tracks the discrete lifecycle states of a trade signal entity from its initial creation to final order confirmation or selective abstention.
</p>
<div class="diagram-container">
  {svg_state}
</div>

<h4>Signal State Transition Matrix</h4>
<table>
  <thead>
    <tr><th>Current State</th><th>Trigger / Event</th><th>Guard Condition <code>[Guard]</code></th><th>Target State</th><th>Action Performed</th></tr>
  </thead>
  <tbody>
    <tr><td><code>IDLE</code></td><td><code>req(ticker)</code></td><td>Ticker is active in catalog</td><td><code>INGESTING_SESSION</code></td><td><code>initiate_data_fetch()</code></td></tr>
    <tr><td><code>INGESTING_SESSION</code></td><td><code>data_fetched</code></td><td>Exchange is closed</td><td><code>INGESTING_SESSION</code></td><td><code>enforce_closing_cross_freeze()</code></td></tr>
    <tr><td><code>INGESTING_SESSION</code></td><td><code>data_clean</code></td><td>Valid OHLCV bars &ge; 30</td><td><code>VECTORIZING_SIGNALS</code></td><td><code>compute_26_features()</code></td></tr>
    <tr><td><code>VECTORIZING_SIGNALS</code></td><td><code>features_ready</code></td><td>Stationarity confirmed (<math xmlns="http://www.w3.org/1998/Math/MathML" display="inline"><mrow><mi>p</mi><mo>&lt;</mo><mn>0.05</mn></mrow></math>)</td><td><code>GPU_INFERENCE</code></td><td><code>tensor.to('cuda')</code></td></tr>
    <tr><td><code>GPU_INFERENCE</code></td><td><code>posteriors_ready</code></td><td>CUDA stream synchronized</td><td><code>CHOW_SELECTIVE_GATING</code></td><td><code>extract_max_confidence()</code></td></tr>
    <tr><td><code>CHOW_SELECTIVE_GATING</code></td><td><code>evaluate_tau</code></td><td><math xmlns="http://www.w3.org/1998/Math/MathML" display="inline"><mrow><mi>g</mi><mo stretchy="false">&#x00028;</mo><mi>x</mi><mo stretchy="false">&#x00029;</mo><mo>&lt;</mo><mn>0.75</mn></mrow></math> (Chop Noise)</td><td><code>ABSTAINED_CASH</code></td><td><code>hold_100_percent_cash()</code></td></tr>
    <tr><td><code>CHOW_SELECTIVE_GATING</code></td><td><code>evaluate_tau</code></td><td><math xmlns="http://www.w3.org/1998/Math/MathML" display="inline"><mrow><mi>g</mi><mo stretchy="false">&#x00028;</mo><mi>x</mi><mo stretchy="false">&#x00029;</mo><mo>&#x02265;</mo><mn>0.75</mn></mrow></math> (High Conviction)</td><td><code>CREDIT_DISTRESS_CHECK</code></td><td><code>solve_merton_altman()</code></td></tr>
    <tr><td><code>CREDIT_DISTRESS_CHECK</code></td><td><code>credit_evaluated</code></td><td><math xmlns="http://www.w3.org/1998/Math/MathML" display="inline"><mrow><mi>Z</mi><mo>&lt;</mo><mn>1.81</mn><mo>&#x02228;</mo><mi>D</mi><mi>D</mi><mo>&lt;</mo><mn>1.5</mn></mrow></math></td><td><code>DISTRESS_VETO_HALT</code></td><td><code>execute_buy_veto()</code></td></tr>
    <tr><td><code>CREDIT_DISTRESS_CHECK</code></td><td><code>credit_evaluated</code></td><td><math xmlns="http://www.w3.org/1998/Math/MathML" display="inline"><mrow><mi>Z</mi><mo>&#x02265;</mo><mn>1.81</mn><mo>&#x02227;</mo><mi>D</mi><mi>D</mi><mo>&#x02265;</mo><mn>1.5</mn></mrow></math></td><td><code>HALF_KELLY_SIZING</code></td><td><code>compute_optimal_fraction()</code></td></tr>
    <tr><td><code>HALF_KELLY_SIZING</code></td><td><code>plan_generated</code></td><td>Fraction &le; 0.20 NAV</td><td><code>ORDER_CONFIRMED</code></td><td><code>publish_websocket_signal()</code></td></tr>
  </tbody>
</table>
"""
    res = template
    res = res.replace("{svg_cls}", svg_cls)
    res = res.replace("{svg_act}", svg_act)
    res = res.replace("{svg_dep}", svg_dep)
    res = res.replace("{svg_comp}", svg_comp)
    res = res.replace("{svg_seq}", svg_seq)
    res = res.replace("{svg_state}", svg_state)
    res = res.replace("{svg_uc}", svg_uc)
    res = res.replace("{svg_col}", svg_col)
    return res
