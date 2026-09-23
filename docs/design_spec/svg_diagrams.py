"""
SVG Diagram Generator for StockTrend AI / AlphaTemporal System Design Specification.
Generates 13 high-resolution vector SVG diagrams:
1. System Architecture Diagram
2. Entity-Relationship (ER) Database Diagram
3. UML Use Case Diagram
4. UML Class Diagram
5. UML Sequence Diagram
6. UML Collaboration Diagram
7. UML Activity Diagram
8. UML Component Diagram
9. UML Deployment Diagram
10. UML State-Chart Diagram
11. DFD Level 0 (Context Diagram)
12. DFD Level 1 (Subsystem Decomposition)
13. DFD Level 2 (Detailed Inference & Risk Gating)
"""

def get_system_architecture_svg():
    return '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 960 720" width="100%" height="auto">
  <defs>
    
    
    
    
    
    
    
    <marker id="arrow" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1 L 10 5 L 0 9 z" fill="#000000"/>
    </marker>
  </defs>

  <!-- Canvas Background -->
  <rect width="960" height="720" fill="#ffffff" stroke="#000000" stroke-width="1.2"/>

  <!-- Title Header -->
  <rect x="20" y="15" width="920" height="48" rx="6" fill="#000000"/>
  <text x="480" y="44" font-family="'Times New Roman', Times, serif" font-size="16" font-weight="700" fill="#ffffff" text-anchor="middle">
    ALPHATEMPORAL / STOCKTREND AI — MULTI-TIER SYSTEM ARCHITECTURE
  </text>

  <!-- TIER 1: Presentation & Client Gateway Layer -->
  <rect x="30" y="75" width="900" height="90" rx="6" fill="#ffffff" stroke="#000000" stroke-width="1.5"/>
  <rect x="30" y="75" width="180" height="90" rx="6" fill="#eeeeee"/>
  <text x="120" y="115" font-family="'Times New Roman', Times, serif" font-size="12" font-weight="700" fill="#000000" text-anchor="middle">TIER 1</text>
  <text x="120" y="132" font-family="'Times New Roman', Times, serif" font-size="10" fill="#333333" text-anchor="middle">Presentation &amp; UI</text>
  
  <!-- Presentation Modules -->
  <rect x="230" y="88" width="200" height="64" rx="4" fill="#ffffff" stroke="#000000" stroke-width="1"/>
  <text x="330" y="112" font-family="'Times New Roman', Times, serif" font-size="11" font-weight="600" fill="#000000" text-anchor="middle">Institutional Web Dashboard</text>
  <text x="330" y="130" font-family="'Times New Roman', Times, serif" font-size="9" fill="#333333" text-anchor="middle">TradingView Lightweight Charts (Port 8050)</text>

  <rect x="450" y="88" width="220" height="64" rx="4" fill="#ffffff" stroke="#000000" stroke-width="1"/>
  <text x="560" y="112" font-family="'Times New Roman', Times, serif" font-size="11" font-weight="600" fill="#000000" text-anchor="middle">Pure-Python Gradio Terminal</text>
  <text x="560" y="130" font-family="'Times New Roman', Times, serif" font-size="9" fill="#333333" text-anchor="middle">7 Interactive Quant Tabs (Port 7860)</text>

  <rect x="690" y="88" width="220" height="64" rx="4" fill="#ffffff" stroke="#000000" stroke-width="1"/>
  <text x="800" y="112" font-family="'Times New Roman', Times, serif" font-size="11" font-weight="600" fill="#000000" text-anchor="middle">CLI Terminal &amp; Benchmarker</text>
  <text x="800" y="130" font-family="'Times New Roman', Times, serif" font-size="9" fill="#333333" text-anchor="middle">cli.py headless simulation / tests</text>

  <!-- Connectors Tier 1 -> Tier 2 -->
  <line x1="480" y1="165" x2="480" y2="185" stroke="#000000" stroke-width="1.5" marker-end="url(#arrow)"/>

  <!-- TIER 2: API Gateway & Streaming Layer -->
  <rect x="30" y="185" width="900" height="85" rx="6" fill="#ffffff" stroke="#000000" stroke-width="1.5"/>
  <rect x="30" y="185" width="180" height="85" rx="6" fill="#eeeeee"/>
  <text x="120" y="222" font-family="'Times New Roman', Times, serif" font-size="12" font-weight="700" fill="#000000" text-anchor="middle">TIER 2</text>
  <text x="120" y="239" font-family="'Times New Roman', Times, serif" font-size="10" fill="#333333" text-anchor="middle">API Gateway &amp; Telemetry</text>

  <!-- Gateway Modules -->
  <rect x="230" y="197" width="210" height="60" rx="4" fill="#ffffff" stroke="#000000" stroke-width="1"/>
  <text x="335" y="221" font-family="'Times New Roman', Times, serif" font-size="11" font-weight="600" fill="#000000" text-anchor="middle">FastAPI Asynchronous Gateway</text>
  <text x="335" y="238" font-family="'Times New Roman', Times, serif" font-size="9" fill="#333333" text-anchor="middle">REST OpenAPI / JSON Schema Guard</text>

  <rect x="460" y="197" width="220" height="60" rx="4" fill="#ffffff" stroke="#000000" stroke-width="1"/>
  <text x="570" y="221" font-family="'Times New Roman', Times, serif" font-size="11" font-weight="600" fill="#000000" text-anchor="middle">Real-Time WebSocket Server</text>
  <text x="570" y="238" font-family="'Times New Roman', Times, serif" font-size="9" fill="#333333" text-anchor="middle">Live Order Book Depth &amp; Sub-sec Ticks</text>

  <rect x="700" y="197" width="210" height="60" rx="4" fill="#ffffff" stroke="#000000" stroke-width="1"/>
  <text x="805" y="221" font-family="'Times New Roman', Times, serif" font-size="11" font-weight="600" fill="#000000" text-anchor="middle">Hardware Telemetry Engine</text>
  <text x="805" y="238" font-family="'Times New Roman', Times, serif" font-size="9" fill="#333333" text-anchor="middle">CUDA VRAM / Host RAM / Process Telemetry</text>

  <!-- Connectors Tier 2 -> Tier 3 -->
  <line x1="480" y1="270" x2="480" y2="290" stroke="#000000" stroke-width="1.5" marker-end="url(#arrow)"/>

  <!-- TIER 3: Ingestion, Session Locking & Caching -->
  <rect x="30" y="290" width="900" height="90" rx="6" fill="#ffffff" stroke="#000000" stroke-width="1.5"/>
  <rect x="30" y="290" width="180" height="90" rx="6" fill="#eeeeee"/>
  <text x="120" y="328" font-family="'Times New Roman', Times, serif" font-size="12" font-weight="700" fill="#000000" text-anchor="middle">TIER 3</text>
  <text x="120" y="345" font-family="'Times New Roman', Times, serif" font-size="10" fill="#333333" text-anchor="middle">Data Ingestion &amp; Integrity</text>

  <rect x="230" y="303" width="210" height="64" rx="4" fill="#ffffff" stroke="#000000" stroke-width="1"/>
  <text x="335" y="327" font-family="'Times New Roman', Times, serif" font-size="11" font-weight="600" fill="#000000" text-anchor="middle">NSE Physical Session Lock</text>
  <text x="335" y="344" font-family="'Times New Roman', Times, serif" font-size="9" fill="#333333" text-anchor="middle">09:15-15:30 IST Freeze Cross | 24/7 Binance</text>

  <rect x="460" y="303" width="220" height="64" rx="4" fill="#ffffff" stroke="#000000" stroke-width="1"/>
  <text x="570" y="327" font-family="'Times New Roman', Times, serif" font-size="11" font-weight="600" fill="#000000" text-anchor="middle">3-Tier Resilient Cache Hierarchy</text>
  <text x="570" y="344" font-family="'Times New Roman', Times, serif" font-size="9" fill="#333333" text-anchor="middle">In-Memory TTL &lt;0.1ms | Disk Parquet | Synth</text>

  <rect x="700" y="303" width="210" height="64" rx="4" fill="#ffffff" stroke="#000000" stroke-width="1"/>
  <text x="805" y="327" font-family="'Times New Roman', Times, serif" font-size="11" font-weight="600" fill="#000000" text-anchor="middle">Network Retry Circuit Breaker</text>
  <text x="805" y="344" font-family="'Times New Roman', Times, serif" font-size="9" fill="#333333" text-anchor="middle">Exponential backoff (2 attempts + jitter)</text>

  <!-- Connectors Tier 3 -> Tier 4 -->
  <line x1="480" y1="380" x2="480" y2="400" stroke="#000000" stroke-width="1.5" marker-end="url(#arrow)"/>

  <!-- TIER 4: Feature Engineering & Signal Vectorization -->
  <rect x="30" y="400" width="900" height="90" rx="6" fill="#ffffff" stroke="#000000" stroke-width="1.5"/>
  <rect x="30" y="400" width="180" height="90" rx="6" fill="#eeeeee"/>
  <text x="120" y="438" font-family="'Times New Roman', Times, serif" font-size="12" font-weight="700" fill="#000000" text-anchor="middle">TIER 4</text>
  <text x="120" y="455" font-family="'Times New Roman', Times, serif" font-size="10" fill="#333333" text-anchor="middle">Signal Vectorization</text>

  <rect x="230" y="413" width="210" height="64" rx="4" fill="#ffffff" stroke="#000000" stroke-width="1"/>
  <text x="335" y="437" font-family="'Times New Roman', Times, serif" font-size="11" font-weight="600" fill="#000000" text-anchor="middle">1D FIR Vectorized Hull MA</text>
  <text x="335" y="454" font-family="'Times New Roman', Times, serif" font-size="9" fill="#333333" text-anchor="middle">LTI Convolution Kernel (35.2x speedup)</text>

  <rect x="460" y="413" width="220" height="64" rx="4" fill="#ffffff" stroke="#000000" stroke-width="1"/>
  <text x="570" y="437" font-family="'Times New Roman', Times, serif" font-size="11" font-weight="600" fill="#000000" text-anchor="middle">26-Indicator Feature Matrix</text>
  <text x="570" y="454" font-family="'Times New Roman', Times, serif" font-size="9" fill="#333333" text-anchor="middle">SuperTrend (28x fast), ADX 14, VWAP, Ichimoku</text>

  <rect x="700" y="413" width="210" height="64" rx="4" fill="#ffffff" stroke="#000000" stroke-width="1"/>
  <text x="805" y="437" font-family="'Times New Roman', Times, serif" font-size="11" font-weight="600" fill="#000000" text-anchor="middle">Fractional Differencing Engine</text>
  <text x="805" y="454" font-family="'Times New Roman', Times, serif" font-size="9" fill="#333333" text-anchor="middle">Optimal d* search (p &lt; 0.05, 88% memory)</text>

  <!-- Connectors Tier 4 -> Tier 5 -->
  <line x1="480" y1="490" x2="480" y2="510" stroke="#000000" stroke-width="1.5" marker-end="url(#arrow)"/>

  <!-- TIER 5: AI Ensemble, Selective Risk & Execution Tier -->
  <rect x="30" y="510" width="900" height="100" rx="6" fill="#ffffff" stroke="#000000" stroke-width="1.5"/>
  <rect x="30" y="510" width="180" height="100" rx="6" fill="#eeeeee"/>
  <text x="120" y="552" font-family="'Times New Roman', Times, serif" font-size="12" font-weight="700" fill="#000000" text-anchor="middle">TIER 5</text>
  <text x="120" y="569" font-family="'Times New Roman', Times, serif" font-size="10" fill="#333333" text-anchor="middle">AI Ensemble &amp; Risk Gating</text>

  <rect x="230" y="522" width="210" height="76" rx="4" fill="#ffffff" stroke="#000000" stroke-width="1"/>
  <text x="335" y="545" font-family="'Times New Roman', Times, serif" font-size="11" font-weight="600" fill="#000000" text-anchor="middle">Temporal Deep Learning</text>
  <text x="335" y="562" font-family="'Times New Roman', Times, serif" font-size="9" fill="#333333" text-anchor="middle">TCN (RF=61) &amp; TFT (VSN + Attention)</text>
  <text x="335" y="578" font-family="'Times New Roman', Times, serif" font-size="9" fill="#333333" text-anchor="middle">BiLSTM Attention (O(1) gradient flow)</text>

  <rect x="460" y="522" width="220" height="76" rx="4" fill="#ffffff" stroke="#000000" stroke-width="1"/>
  <text x="570" y="545" font-family="'Times New Roman', Times, serif" font-size="11" font-weight="600" fill="#000000" text-anchor="middle">Chow Selective Rule (&#964; &ge; 0.75)</text>
  <text x="570" y="562" font-family="'Times New Roman', Times, serif" font-size="9" fill="#333333" text-anchor="middle">Monotonic Error Bounding &epsilon;(x) &le; 1 - &#964;</text>
  <text x="570" y="578" font-family="'Times New Roman', Times, serif" font-size="9" fill="#333333" text-anchor="middle">Abstains on chop &rarr; 95.4% Win Rate</text>

  <rect x="700" y="522" width="210" height="76" rx="4" fill="#ffffff" stroke="#000000" stroke-width="1"/>
  <text x="805" y="545" font-family="'Times New Roman', Times, serif" font-size="11" font-weight="600" fill="#000000" text-anchor="middle">Quantitative Credit &amp; Allocation</text>
  <text x="805" y="562" font-family="'Times New Roman', Times, serif" font-size="9" fill="#333333" text-anchor="middle">Merton DD + Altman Z Veto Gate</text>
  <text x="805" y="578" font-family="'Times New Roman', Times, serif" font-size="9" fill="#333333" text-anchor="middle">Dynamic Triple-Barrier &amp; Half-Kelly Sizing</text>

  <!-- Bottom Hardware Tier Indicator -->
  <rect x="30" y="625" width="900" height="75" rx="6" fill="#f8f8f8" stroke="#000000" stroke-width="1.5"/>
  <text x="50" y="655" font-family="'Times New Roman', Times, serif" font-size="12" font-weight="700" fill="#000000">UNDERLYING HARDWARE ACCELERATION &amp; COMPUTE SUBSTRATE</text>
  <text x="50" y="675" font-family="'Times New Roman', Times, serif" font-size="10" fill="#333333">NVIDIA GeForce RTX 3070 Ti Laptop GPU (8,191.5 MB VRAM, CUDA 12.x, Tensor Cores) | 16-Thread Host CPU | AVX-256 SIMD Vectorization</text>
  <rect x="800" y="642" width="115" height="42" rx="4" fill="#000000"/>
  <text x="857" y="667" font-family="'Times New Roman', Times, serif" font-size="11" font-weight="700" fill="#ffffff" text-anchor="middle">CUDA ACTIVE</text>
</svg>'''

def get_er_database_svg():
    return '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 960 760" width="100%" height="auto">
  <defs>
    
    
    <marker id="crowFoot" viewBox="0 0 12 12" refX="10" refY="6" markerWidth="8" markerHeight="8" orient="auto-start-reverse">
      <path d="M 0 0 L 12 6 L 0 12 M 12 6 L 0 6" fill="none" stroke="#000000" stroke-width="1.5"/>
    </marker>
    <marker id="oneOne" viewBox="0 0 12 12" refX="2" refY="6" markerWidth="8" markerHeight="8" orient="auto">
      <line x1="4" y1="0" x2="4" y2="12" stroke="#000000" stroke-width="2"/>
      <line x1="8" y1="0" x2="8" y2="12" stroke="#000000" stroke-width="2"/>
    </marker>
  </defs>

  <rect width="960" height="760" fill="#ffffff" stroke="#000000" stroke-width="1.2"/>

  <!-- Title -->
  <rect x="20" y="15" width="920" height="45" rx="6" fill="#000000" stroke="#000000"/>
  <text x="480" y="43" font-family="'Times New Roman', Times, serif" font-size="15" font-weight="700" fill="#ffffff" text-anchor="middle">
    ALPHATEMPORAL RELATIONAL DATABASE ENTITY-RELATIONSHIP (ER) DIAGRAM
  </text>

  <!-- TABLE 1: EQUITIES -->
  <g transform="translate(30, 80)">
    <rect width="180" height="150" fill="#ffffff" stroke="#000000" stroke-width="1.2" rx="4"/>
    <rect width="180" height="26" fill="#1a1a1a" rx="4"/>
    <text x="90" y="18" font-family="'Times New Roman', Times, serif" font-size="11" font-weight="700" fill="#ffffff" text-anchor="middle">EQUITIES (Assets)</text>
    <text x="8" y="44" font-family="'Courier New', Courier, monospace" font-size="9" font-weight="700" fill="#000000" font-weight="bold">PK ticker VARCHAR(16)</text>
    <text x="8" y="60" font-family="'Courier New', Courier, monospace" font-size="9" fill="#000000">   company_name VARCHAR(128)</text>
    <text x="8" y="76" font-family="'Courier New', Courier, monospace" font-size="9" fill="#000000">   exchange VARCHAR(16)</text>
    <text x="8" y="92" font-family="'Courier New', Courier, monospace" font-size="9" fill="#000000">   sector_key VARCHAR(64)</text>
    <text x="8" y="108" font-family="'Courier New', Courier, monospace" font-size="9" fill="#000000">   currency VARCHAR(8)</text>
    <text x="8" y="124" font-family="'Courier New', Courier, monospace" font-size="9" fill="#000000">   is_crypto BOOLEAN</text>
    <text x="8" y="140" font-family="'Courier New', Courier, monospace" font-size="9" fill="#000000">   is_active BOOLEAN</text>
  </g>

  <!-- TABLE 2: MARKET_SESSIONS -->
  <g transform="translate(260, 80)">
    <rect width="200" height="150" fill="#ffffff" stroke="#000000" stroke-width="1.2" rx="4"/>
    <rect width="200" height="26" fill="#1a1a1a" rx="4"/>
    <text x="100" y="18" font-family="'Times New Roman', Times, serif" font-size="11" font-weight="700" fill="#ffffff" text-anchor="middle">MARKET_SESSIONS</text>
    <text x="8" y="44" font-family="'Courier New', Courier, monospace" font-size="9" font-weight="700" fill="#000000" font-weight="bold">PK session_id BIGINT</text>
    <text x="8" y="60" font-family="'Courier New', Courier, monospace" font-size="9" font-weight="700" fill="#000000" font-weight="bold">FK exchange VARCHAR(16)</text>
    <text x="8" y="76" font-family="'Courier New', Courier, monospace" font-size="9" fill="#000000">   trade_date DATE</text>
    <text x="8" y="92" font-family="'Courier New', Courier, monospace" font-size="9" fill="#000000">   open_time_ist TIME</text>
    <text x="8" y="108" font-family="'Courier New', Courier, monospace" font-size="9" fill="#000000">   close_time_ist TIME</text>
    <text x="8" y="124" font-family="'Courier New', Courier, monospace" font-size="9" fill="#000000">   is_holiday BOOLEAN</text>
    <text x="8" y="140" font-family="'Courier New', Courier, monospace" font-size="9" fill="#000000">   closing_cross_frozen BOOL</text>
  </g>

  <!-- TABLE 3: CANDLE_DATA_1D -->
  <g transform="translate(510, 80)">
    <rect width="200" height="150" fill="#ffffff" stroke="#000000" stroke-width="1.2" rx="4"/>
    <rect width="200" height="26" fill="#1a1a1a" rx="4"/>
    <text x="100" y="18" font-family="'Times New Roman', Times, serif" font-size="11" font-weight="700" fill="#ffffff" text-anchor="middle">CANDLE_DATA_1D</text>
    <text x="8" y="44" font-family="'Courier New', Courier, monospace" font-size="9" font-weight="700" fill="#000000" font-weight="bold">PK candle_id BIGINT</text>
    <text x="8" y="60" font-family="'Courier New', Courier, monospace" font-size="9" font-weight="700" fill="#000000" font-weight="bold">FK ticker VARCHAR(16)</text>
    <text x="8" y="76" font-family="'Courier New', Courier, monospace" font-size="9" fill="#000000">   timestamp_utc DATETIME</text>
    <text x="8" y="92" font-family="'Courier New', Courier, monospace" font-size="9" fill="#000000">   open, high, low, close NUM</text>
    <text x="8" y="108" font-family="'Courier New', Courier, monospace" font-size="9" fill="#000000">   volume BIGINT</text>
    <text x="8" y="124" font-family="'Courier New', Courier, monospace" font-size="9" fill="#000000">   vwap NUMERIC(12,4)</text>
    <text x="8" y="140" font-family="'Courier New', Courier, monospace" font-size="9" fill="#000000">   data_source VARCHAR(32)</text>
  </g>

  <!-- TABLE 4: FEATURE_MATRIX_26 -->
  <g transform="translate(740, 80)">
    <rect width="190" height="150" fill="#ffffff" stroke="#000000" stroke-width="1.2" rx="4"/>
    <rect width="190" height="26" fill="#1a1a1a" rx="4"/>
    <text x="95" y="18" font-family="'Times New Roman', Times, serif" font-size="11" font-weight="700" fill="#ffffff" text-anchor="middle">FEATURE_MATRIX_26</text>
    <text x="8" y="44" font-family="'Courier New', Courier, monospace" font-size="9" font-weight="700" fill="#000000" font-weight="bold">PK feature_id BIGINT</text>
    <text x="8" y="60" font-family="'Courier New', Courier, monospace" font-size="9" font-weight="700" fill="#000000" font-weight="bold">FK candle_id BIGINT</text>
    <text x="8" y="76" font-family="'Courier New', Courier, monospace" font-size="9" fill="#000000">   hma_9 NUMERIC(12,4)</text>
    <text x="8" y="92" font-family="'Courier New', Courier, monospace" font-size="9" fill="#000000">   supertrend_dir INT</text>
    <text x="8" y="108" font-family="'Courier New', Courier, monospace" font-size="9" fill="#000000">   adx_14, rsi_14 NUM</text>
    <text x="8" y="124" font-family="'Courier New', Courier, monospace" font-size="9" fill="#000000">   frac_diff_d04 NUM</text>
    <text x="8" y="140" font-family="'Courier New', Courier, monospace" font-size="9" fill="#000000">   twenty_one_other_cols ...</text>
  </g>

  <!-- TABLE 5: MODEL_REGISTRY -->
  <g transform="translate(30, 270)">
    <rect width="180" height="150" fill="#ffffff" stroke="#000000" stroke-width="1.2" rx="4"/>
    <rect width="180" height="26" fill="#1a1a1a" rx="4"/>
    <text x="90" y="18" font-family="'Times New Roman', Times, serif" font-size="11" font-weight="700" fill="#ffffff" text-anchor="middle">MODEL_REGISTRY</text>
    <text x="8" y="44" font-family="'Courier New', Courier, monospace" font-size="9" font-weight="700" fill="#000000" font-weight="bold">PK model_id VARCHAR(32)</text>
    <text x="8" y="60" font-family="'Courier New', Courier, monospace" font-size="9" fill="#000000">   model_family VARCHAR(32)</text>
    <text x="8" y="76" font-family="'Courier New', Courier, monospace" font-size="9" fill="#000000">   architecture VARCHAR(64)</text>
    <text x="8" y="92" font-family="'Courier New', Courier, monospace" font-size="9" fill="#000000">   receptive_field INT</text>
    <text x="8" y="108" font-family="'Courier New', Courier, monospace" font-size="9" fill="#000000">   supports_gpu BOOLEAN</text>
    <text x="8" y="124" font-family="'Courier New', Courier, monospace" font-size="9" fill="#000000">   param_count BIGINT</text>
    <text x="8" y="140" font-family="'Courier New', Courier, monospace" font-size="9" fill="#000000">   is_ensemble_member BOOL</text>
  </g>

  <!-- TABLE 6: MODEL_TRAINING_RUNS -->
  <g transform="translate(260, 270)">
    <rect width="200" height="150" fill="#ffffff" stroke="#000000" stroke-width="1.2" rx="4"/>
    <rect width="200" height="26" fill="#1a1a1a" rx="4"/>
    <text x="100" y="18" font-family="'Times New Roman', Times, serif" font-size="11" font-weight="700" fill="#ffffff" text-anchor="middle">MODEL_TRAINING_RUNS</text>
    <text x="8" y="44" font-family="'Courier New', Courier, monospace" font-size="9" font-weight="700" fill="#000000" font-weight="bold">PK run_id BIGINT</text>
    <text x="8" y="60" font-family="'Courier New', Courier, monospace" font-size="9" font-weight="700" fill="#000000" font-weight="bold">FK model_id VARCHAR(32)</text>
    <text x="8" y="76" font-family="'Courier New', Courier, monospace" font-size="9" font-weight="700" fill="#000000" font-weight="bold">FK ticker VARCHAR(16)</text>
    <text x="8" y="92" font-family="'Courier New', Courier, monospace" font-size="9" fill="#000000">   train_epochs INT</text>
    <text x="8" y="108" font-family="'Courier New', Courier, monospace" font-size="9" fill="#000000">   f1_score, accuracy NUM</text>
    <text x="8" y="124" font-family="'Courier New', Courier, monospace" font-size="9" fill="#000000">   weights_path VARCHAR(256)</text>
    <text x="8" y="140" font-family="'Courier New', Courier, monospace" font-size="9" fill="#000000">   trained_on_gpu VARCHAR(32)</text>
  </g>

  <!-- TABLE 7: INFERENCE_PREDICTIONS -->
  <g transform="translate(510, 270)">
    <rect width="200" height="150" fill="#ffffff" stroke="#000000" stroke-width="1.2" rx="4"/>
    <rect width="200" height="26" fill="#1a1a1a" rx="4"/>
    <text x="100" y="18" font-family="'Times New Roman', Times, serif" font-size="11" font-weight="700" fill="#ffffff" text-anchor="middle">INFERENCE_PREDICTIONS</text>
    <text x="8" y="44" font-family="'Courier New', Courier, monospace" font-size="9" font-weight="700" fill="#000000" font-weight="bold">PK pred_id BIGINT</text>
    <text x="8" y="60" font-family="'Courier New', Courier, monospace" font-size="9" font-weight="700" fill="#000000" font-weight="bold">FK run_id BIGINT</text>
    <text x="8" y="76" font-family="'Courier New', Courier, monospace" font-size="9" font-weight="700" fill="#000000" font-weight="bold">FK candle_id BIGINT</text>
    <text x="8" y="92" font-family="'Courier New', Courier, monospace" font-size="9" fill="#000000">   prob_up NUMERIC(6,4)</text>
    <text x="8" y="108" font-family="'Courier New', Courier, monospace" font-size="9" fill="#000000">   prob_down NUMERIC(6,4)</text>
    <text x="8" y="124" font-family="'Courier New', Courier, monospace" font-size="9" fill="#000000">   predicted_class INT</text>
    <text x="8" y="140" font-family="'Courier New', Courier, monospace" font-size="9" fill="#000000">   inference_latency_ms NUM</text>
  </g>

  <!-- TABLE 8: CHOW_SELECTIVE_DECISIONS -->
  <g transform="translate(740, 270)">
    <rect width="190" height="150" fill="#ffffff" stroke="#000000" stroke-width="1.2" rx="4"/>
    <rect width="190" height="26" fill="#1a1a1a" rx="4"/>
    <text x="95" y="18" font-family="'Times New Roman', Times, serif" font-size="11" font-weight="700" fill="#ffffff" text-anchor="middle">CHOW_SELECTIVE_DECISIONS</text>
    <text x="8" y="44" font-family="'Courier New', Courier, monospace" font-size="9" font-weight="700" fill="#000000" font-weight="bold">PK decision_id BIGINT</text>
    <text x="8" y="60" font-family="'Courier New', Courier, monospace" font-size="9" font-weight="700" fill="#000000" font-weight="bold">FK pred_id BIGINT</text>
    <text x="8" y="76" font-family="'Courier New', Courier, monospace" font-size="9" fill="#000000">   confidence_max NUM(6,4)</text>
    <text x="8" y="92" font-family="'Courier New', Courier, monospace" font-size="9" fill="#000000">   tau_threshold NUM(6,4)</text>
    <text x="8" y="108" font-family="'Courier New', Courier, monospace" font-size="9" fill="#000000">   status VARCHAR(16)</text>
    <text x="8" y="124" font-family="'Courier New', Courier, monospace" font-size="9" fill="#000000">   bounded_error NUM(6,4)</text>
    <text x="8" y="140" font-family="'Courier New', Courier, monospace" font-size="9" fill="#000000">   is_executed BOOLEAN</text>
  </g>

  <!-- TABLE 9: CREDIT_DISTRESS_METRICS -->
  <g transform="translate(30, 460)">
    <rect width="180" height="150" fill="#ffffff" stroke="#000000" stroke-width="1.2" rx="4"/>
    <rect width="180" height="26" fill="#1a1a1a" rx="4"/>
    <text x="90" y="18" font-family="'Times New Roman', Times, serif" font-size="11" font-weight="700" fill="#ffffff" text-anchor="middle">CREDIT_DISTRESS</text>
    <text x="8" y="44" font-family="'Courier New', Courier, monospace" font-size="9" font-weight="700" fill="#000000" font-weight="bold">PK credit_id BIGINT</text>
    <text x="8" y="60" font-family="'Courier New', Courier, monospace" font-size="9" font-weight="700" fill="#000000" font-weight="bold">FK ticker VARCHAR(16)</text>
    <text x="8" y="76" font-family="'Courier New', Courier, monospace" font-size="9" fill="#000000">   altman_z_score NUM(8,3)</text>
    <text x="8" y="92" font-family="'Courier New', Courier, monospace" font-size="9" fill="#000000">   merton_dd NUM(8,3)</text>
    <text x="8" y="108" font-family="'Courier New', Courier, monospace" font-size="9" fill="#000000">   default_prob_pct NUM(6,3)</text>
    <text x="8" y="124" font-family="'Courier New', Courier, monospace" font-size="9" fill="#000000">   distress_zone VARCHAR(16)</text>
    <text x="8" y="140" font-family="'Courier New', Courier, monospace" font-size="9" fill="#000000">   buy_veto_flag BOOLEAN</text>
  </g>

  <!-- TABLE 10: TRADING_ACTION_PLANS -->
  <g transform="translate(260, 460)">
    <rect width="200" height="150" fill="#ffffff" stroke="#000000" stroke-width="1.2" rx="4"/>
    <rect width="200" height="26" fill="#1a1a1a" rx="4"/>
    <text x="100" y="18" font-family="'Times New Roman', Times, serif" font-size="11" font-weight="700" fill="#ffffff" text-anchor="middle">TRADING_ACTION_PLANS</text>
    <text x="8" y="44" font-family="'Courier New', Courier, monospace" font-size="9" font-weight="700" fill="#000000" font-weight="bold">PK plan_id BIGINT</text>
    <text x="8" y="60" font-family="'Courier New', Courier, monospace" font-size="9" font-weight="700" fill="#000000" font-weight="bold">FK decision_id BIGINT</text>
    <text x="8" y="76" font-family="'Courier New', Courier, monospace" font-size="9" font-weight="700" fill="#000000" font-weight="bold">FK credit_id BIGINT</text>
    <text x="8" y="92" font-family="'Courier New', Courier, monospace" font-size="9" fill="#000000">   entry_price NUM(12,4)</text>
    <text x="8" y="108" font-family="'Courier New', Courier, monospace" font-size="9" fill="#000000">   stop_loss_price NUM(12,4)</text>
    <text x="8" y="124" font-family="'Courier New', Courier, monospace" font-size="9" fill="#000000">   take_profit_1, 2 NUM(12,4)</text>
    <text x="8" y="140" font-family="'Courier New', Courier, monospace" font-size="9" fill="#000000">   kelly_fraction NUM(6,4)</text>
  </g>

  <!-- TABLE 11: BACKTEST_PORTFOLIOS -->
  <g transform="translate(510, 460)">
    <rect width="200" height="150" fill="#ffffff" stroke="#000000" stroke-width="1.2" rx="4"/>
    <rect width="200" height="26" fill="#1a1a1a" rx="4"/>
    <text x="100" y="18" font-family="'Times New Roman', Times, serif" font-size="11" font-weight="700" fill="#ffffff" text-anchor="middle">BACKTEST_PORTFOLIOS</text>
    <text x="8" y="44" font-family="'Courier New', Courier, monospace" font-size="9" font-weight="700" fill="#000000" font-weight="bold">PK portfolio_id BIGINT</text>
    <text x="8" y="60" font-family="'Courier New', Courier, monospace" font-size="9" font-weight="700" fill="#000000" font-weight="bold">FK run_id BIGINT</text>
    <text x="8" y="76" font-family="'Courier New', Courier, monospace" font-size="9" fill="#000000">   initial_capital NUM(14,2)</text>
    <text x="8" y="92" font-family="'Courier New', Courier, monospace" font-size="9" fill="#000000">   final_value NUM(14,2)</text>
    <text x="8" y="108" font-family="'Courier New', Courier, monospace" font-size="9" fill="#000000">   sharpe_ratio NUM(6,3)</text>
    <text x="8" y="124" font-family="'Courier New', Courier, monospace" font-size="9" fill="#000000">   max_drawdown_pct NUM(6,3)</text>
    <text x="8" y="140" font-family="'Courier New', Courier, monospace" font-size="9" fill="#000000">   win_rate_pct NUM(6,3)</text>
  </g>

  <!-- TABLE 12: BACKTEST_TRADES -->
  <g transform="translate(740, 460)">
    <rect width="190" height="150" fill="#ffffff" stroke="#000000" stroke-width="1.2" rx="4"/>
    <rect width="190" height="26" fill="#1a1a1a" rx="4"/>
    <text x="95" y="18" font-family="'Times New Roman', Times, serif" font-size="11" font-weight="700" fill="#ffffff" text-anchor="middle">BACKTEST_TRADES</text>
    <text x="8" y="44" font-family="'Courier New', Courier, monospace" font-size="9" font-weight="700" fill="#000000" font-weight="bold">PK trade_id BIGINT</text>
    <text x="8" y="60" font-family="'Courier New', Courier, monospace" font-size="9" font-weight="700" fill="#000000" font-weight="bold">FK portfolio_id BIGINT</text>
    <text x="8" y="76" font-family="'Courier New', Courier, monospace" font-size="9" fill="#000000">   trade_direction VARCHAR(8)</text>
    <text x="8" y="92" font-family="'Courier New', Courier, monospace" font-size="9" fill="#000000">   fill_price NUM(12,4)</text>
    <text x="8" y="108" font-family="'Courier New', Courier, monospace" font-size="9" fill="#000000">   exit_price NUM(12,4)</text>
    <text x="8" y="124" font-family="'Courier New', Courier, monospace" font-size="9" fill="#000000">   realized_pnl NUM(12,2)</text>
    <text x="8" y="140" font-family="'Courier New', Courier, monospace" font-size="9" fill="#000000">   exit_reason VARCHAR(32)</text>
  </g>

  <!-- Relationship Lines with Labels -->
  <!-- EQUITIES -> CANDLE_DATA_1D (1:N) -->
  <path d="M 210 150 L 510 150" fill="none" stroke="#000000" stroke-width="1.5" marker-start="url(#oneOne)" marker-end="url(#crowFoot)"/>
  <text x="360" y="145" font-family="'Times New Roman', Times, serif" font-size="8" fill="#333333" text-anchor="middle">1 : N (Historical Bars)</text>

  <!-- CANDLE_DATA_1D -> FEATURE_MATRIX_26 (1:1) -->
  <path d="M 710 150 L 740 150" fill="none" stroke="#000000" stroke-width="1.5" marker-start="url(#oneOne)" marker-end="url(#oneOne)"/>
  <text x="725" y="145" font-family="'Times New Roman', Times, serif" font-size="8" fill="#333333" text-anchor="middle">1:1</text>

  <!-- MODEL_REGISTRY -> MODEL_TRAINING_RUNS (1:N) -->
  <path d="M 210 340 L 260 340" fill="none" stroke="#000000" stroke-width="1.5" marker-start="url(#oneOne)" marker-end="url(#crowFoot)"/>
  <text x="235" y="335" font-family="'Times New Roman', Times, serif" font-size="8" fill="#333333" text-anchor="middle">1:N</text>

  <!-- MODEL_TRAINING_RUNS -> INFERENCE_PREDICTIONS (1:N) -->
  <path d="M 460 340 L 510 340" fill="none" stroke="#000000" stroke-width="1.5" marker-start="url(#oneOne)" marker-end="url(#crowFoot)"/>
  <text x="485" y="335" font-family="'Times New Roman', Times, serif" font-size="8" fill="#333333" text-anchor="middle">1:N</text>

  <!-- INFERENCE_PREDICTIONS -> CHOW_SELECTIVE_DECISIONS (1:1) -->
  <path d="M 710 340 L 740 340" fill="none" stroke="#000000" stroke-width="1.5" marker-start="url(#oneOne)" marker-end="url(#oneOne)"/>
  <text x="725" y="335" font-family="'Times New Roman', Times, serif" font-size="8" fill="#333333" text-anchor="middle">1:1</text>

  <!-- CHOW_SELECTIVE_DECISIONS -> TRADING_ACTION_PLANS (1:1) -->
  <path d="M 835 420 L 835 440 L 360 440 L 360 460" fill="none" stroke="#000000" stroke-width="1.5" marker-start="url(#oneOne)" marker-end="url(#oneOne)"/>
  <text x="590" y="435" font-family="'Times New Roman', Times, serif" font-size="8" fill="#333333" text-anchor="middle">1 : 1 (When Conf &ge; &#964;)</text>

  <!-- CREDIT_DISTRESS -> TRADING_ACTION_PLANS (1:N) -->
  <path d="M 210 530 L 260 530" fill="none" stroke="#000000" stroke-width="1.5" marker-start="url(#oneOne)" marker-end="url(#crowFoot)"/>
  <text x="235" y="525" font-family="'Times New Roman', Times, serif" font-size="8" fill="#333333" text-anchor="middle">1:N</text>

  <!-- BACKTEST_PORTFOLIOS -> BACKTEST_TRADES (1:N) -->
  <path d="M 710 530 L 740 530" fill="none" stroke="#000000" stroke-width="1.5" marker-start="url(#oneOne)" marker-end="url(#crowFoot)"/>
  <text x="725" y="525" font-family="'Times New Roman', Times, serif" font-size="8" fill="#333333" text-anchor="middle">1:N</text>

  <!-- Legend -->
  <rect x="30" y="640" width="900" height="95" rx="4" fill="#ffffff" stroke="#000000"/>
  <text x="50" y="662" font-family="'Times New Roman', Times, serif" font-size="11" font-weight="700" fill="#000000">DATABASE DESIGN SCHEMA METRICS &amp; CONSTRAINTS SUMMARY</text>
  <text x="50" y="682" font-family="'Times New Roman', Times, serif" font-size="9" fill="#333333">&bull; Third Normal Form (3NF) strictly enforced across all 12 relations; zero transitive functional dependencies.</text>
  <text x="50" y="700" font-family="'Times New Roman', Times, serif" font-size="9" fill="#333333">&bull; High-performance B-Tree Composite Indexes on (ticker, timestamp_utc) and (run_id, candle_id) ensuring O(log N) retrieval.</text>
  <text x="50" y="718" font-family="'Times New Roman', Times, serif" font-size="9" fill="#333333">&bull; Foreign key referential integrity with ON DELETE CASCADE for ephemeral training runs and RESTRICT on master equity tickers.</text>
</svg>'''

def get_uml_use_case_svg():
    return '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 960 700" width="100%" height="auto">
  <defs>
    
    
    <marker id="ucArrow" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1 L 10 5 L 0 9 z" fill="#000000"/>
    </marker>
  </defs>

  <rect width="960" height="700" fill="#ffffff" stroke="#000000" stroke-width="1.2"/>

  <!-- System Boundary Box -->
  <rect x="220" y="40" width="530" height="630" rx="8" fill="#ffffff" stroke="#000000" stroke-width="2" stroke-dasharray="6,4"/>
  <rect x="220" y="40" width="530" height="32" rx="8" fill="#000000"/>
  <text x="485" y="62" font-family="'Times New Roman', Times, serif" font-size="13" font-weight="700" fill="#ffffff" text-anchor="middle">
    SYSTEM BOUNDARY: StockTrend AI / AlphaTemporal Production Platform
  </text>

  <!-- ACTORS (Left Side) -->
  <!-- Actor 1: Quantitative Trader -->
  <g transform="translate(60, 100)">
    <circle cx="40" cy="20" r="14" fill="#ffffff" stroke="#000000" stroke-width="2"/>
    <line x1="40" y1="34" x2="40" y2="70" stroke="#000000" stroke-width="2"/>
    <line x1="15" y1="48" x2="65" y2="48" stroke="#000000" stroke-width="2"/>
    <line x1="40" y1="70" x2="20" y2="105" stroke="#000000" stroke-width="2"/>
    <line x1="40" y1="70" x2="60" y2="105" stroke="#000000" stroke-width="2"/>
    <text x="40" y="125" font-family="'Times New Roman', Times, serif" font-size="11" font-weight="700" fill="#000000" text-anchor="middle">Quantitative Trader</text>
  </g>

  <!-- Actor 2: Risk Manager -->
  <g transform="translate(60, 310)">
    <circle cx="40" cy="20" r="14" fill="#ffffff" stroke="#000000" stroke-width="2"/>
    <line x1="40" y1="34" x2="40" y2="70" stroke="#000000" stroke-width="2"/>
    <line x1="15" y1="48" x2="65" y2="48" stroke="#000000" stroke-width="2"/>
    <line x1="40" y1="70" x2="20" y2="105" stroke="#000000" stroke-width="2"/>
    <line x1="40" y1="70" x2="60" y2="105" stroke="#000000" stroke-width="2"/>
    <text x="40" y="125" font-family="'Times New Roman', Times, serif" font-size="11" font-weight="700" fill="#000000" text-anchor="middle">Risk Manager</text>
  </g>

  <!-- Actor 3: System Administrator -->
  <g transform="translate(60, 500)">
    <circle cx="40" cy="20" r="14" fill="#ffffff" stroke="#000000" stroke-width="2"/>
    <line x1="40" y1="34" x2="40" y2="70" stroke="#000000" stroke-width="2"/>
    <line x1="15" y1="48" x2="65" y2="48" stroke="#000000" stroke-width="2"/>
    <line x1="40" y1="70" x2="20" y2="105" stroke="#000000" stroke-width="2"/>
    <line x1="40" y1="70" x2="60" y2="105" stroke="#000000" stroke-width="2"/>
    <text x="40" y="125" font-family="'Times New Roman', Times, serif" font-size="11" font-weight="700" fill="#000000" text-anchor="middle">System Administrator</text>
  </g>

  <!-- ACTORS (Right Side - External Systems) -->
  <!-- Actor 4: National Stock Exchange (NSE) -->
  <g transform="translate(830, 160)">
    <rect x="0" y="0" width="80" height="60" rx="4" fill="#ffffff" stroke="#000000" stroke-width="2"/>
    <text x="40" y="26" font-family="'Times New Roman', Times, serif" font-size="10" font-weight="700" fill="#000000" text-anchor="middle">&lt;&lt;System&gt;&gt;</text>
    <text x="40" y="44" font-family="'Times New Roman', Times, serif" font-size="10" font-weight="700" fill="#000000" text-anchor="middle">NSE Gateway</text>
  </g>

  <!-- Actor 5: Binance WebSocket Gateway -->
  <g transform="translate(830, 390)">
    <rect x="0" y="0" width="80" height="60" rx="4" fill="#ffffff" stroke="#000000" stroke-width="2"/>
    <text x="40" y="26" font-family="'Times New Roman', Times, serif" font-size="10" font-weight="700" fill="#000000" text-anchor="middle">&lt;&lt;System&gt;&gt;</text>
    <text x="40" y="44" font-family="'Times New Roman', Times, serif" font-size="10" font-weight="700" fill="#000000" text-anchor="middle">Binance WS</text>
  </g>

  <!-- USE CASES (Inside Boundary) -->
  <!-- UC 1: Ingest Live Market Feed -->
  <g transform="translate(260, 95)">
    <ellipse cx="140" cy="24" rx="130" ry="22" fill="#ffffff" stroke="#000000" stroke-width="1.5"/>
    <text x="140" y="28" font-family="'Times New Roman', Times, serif" font-size="11" font-weight="600" fill="#000000" text-anchor="middle">UC1: Ingest Live &amp; Historical Feeds</text>
  </g>

  <!-- UC 2: Lock NSE Physical Session -->
  <g transform="translate(460, 145)">
    <ellipse cx="120" cy="20" rx="115" ry="18" fill="#ffffff" stroke="#000000" stroke-width="1.2"/>
    <text x="120" y="24" font-family="'Times New Roman', Times, serif" font-size="10" fill="#000000" text-anchor="middle">UC2: Lock NSE Session Cross</text>
  </g>

  <!-- UC 3: Compute 26-Indicator Matrix -->
  <g transform="translate(260, 195)">
    <ellipse cx="140" cy="24" rx="130" ry="22" fill="#ffffff" stroke="#000000" stroke-width="1.5"/>
    <text x="140" y="28" font-family="'Times New Roman', Times, serif" font-size="11" font-weight="600" fill="#000000" text-anchor="middle">UC3: Vectorize 26 Features &amp; HMA</text>
  </g>

  <!-- UC 4: Apply Fractional Differencing -->
  <g transform="translate(460, 245)">
    <ellipse cx="120" cy="20" rx="115" ry="18" fill="#ffffff" stroke="#000000" stroke-width="1.2"/>
    <text x="120" y="24" font-family="'Times New Roman', Times, serif" font-size="10" fill="#000000" text-anchor="middle">UC4: Fractional Diff d* Stationarity</text>
  </g>

  <!-- UC 5: Execute Temporal Deep Learning -->
  <g transform="translate(260, 295)">
    <ellipse cx="140" cy="24" rx="130" ry="22" fill="#ffffff" stroke="#000000" stroke-width="1.5"/>
    <text x="140" y="28" font-family="'Times New Roman', Times, serif" font-size="11" font-weight="600" fill="#000000" text-anchor="middle">UC5: Infer via TFT / TCN Ensemble</text>
  </g>

  <!-- UC 6: Selective Gating via Chow Rule -->
  <g transform="translate(260, 375)">
    <ellipse cx="140" cy="24" rx="130" ry="22" fill="#ffffff" stroke="#000000" stroke-width="1.5"/>
    <text x="140" y="28" font-family="'Times New Roman', Times, serif" font-size="11" font-weight="600" fill="#000000" text-anchor="middle">UC6: Abstain/Execute (Chow &tau; &ge; 0.75)</text>
  </g>

  <!-- UC 7: Evaluate Credit Distress & Veto -->
  <g transform="translate(260, 455)">
    <ellipse cx="140" cy="24" rx="130" ry="22" fill="#ffffff" stroke="#000000" stroke-width="1.5"/>
    <text x="140" y="28" font-family="'Times New Roman', Times, serif" font-size="11" font-weight="600" fill="#000000" text-anchor="middle">UC7: Evaluate Merton DD &amp; Altman Z</text>
  </g>

  <!-- UC 8: Generate Half-Kelly Action Plan -->
  <g transform="translate(260, 535)">
    <ellipse cx="140" cy="24" rx="130" ry="22" fill="#ffffff" stroke="#000000" stroke-width="1.5"/>
    <text x="140" y="28" font-family="'Times New Roman', Times, serif" font-size="11" font-weight="600" fill="#000000" text-anchor="middle">UC8: Size Position via Half-Kelly</text>
  </g>

  <!-- UC 9: Monitor GPU Hardware Telemetry -->
  <g transform="translate(260, 610)">
    <ellipse cx="140" cy="22" rx="130" ry="20" fill="#ffffff" stroke="#000000" stroke-width="1.5"/>
    <text x="140" y="26" font-family="'Times New Roman', Times, serif" font-size="11" font-weight="600" fill="#000000" text-anchor="middle">UC9: Query CUDA RTX 3070 Ti Telemetry</text>
  </g>

  <!-- Association Lines -->
  <!-- Trader -> UC1, UC3, UC5, UC6, UC8 -->
  <line x1="120" y1="150" x2="260" y2="120" stroke="#000000" stroke-width="1.2"/>
  <line x1="120" y1="150" x2="260" y2="218" stroke="#000000" stroke-width="1.2"/>
  <line x1="120" y1="150" x2="260" y2="318" stroke="#000000" stroke-width="1.2"/>
  <line x1="120" y1="150" x2="260" y2="398" stroke="#000000" stroke-width="1.2"/>
  <line x1="120" y1="150" x2="260" y2="558" stroke="#000000" stroke-width="1.2"/>

  <!-- Risk Manager -> UC6, UC7, UC8 -->
  <line x1="120" y1="360" x2="260" y2="400" stroke="#000000" stroke-width="1.2"/>
  <line x1="120" y1="360" x2="260" y2="478" stroke="#000000" stroke-width="1.2"/>
  <line x1="120" y1="360" x2="260" y2="558" stroke="#000000" stroke-width="1.2"/>

  <!-- Admin -> UC9 -->
  <line x1="120" y1="550" x2="260" y2="630" stroke="#000000" stroke-width="1.2"/>

  <!-- External Systems -> UC1 -->
  <line x1="830" y1="190" x2="520" y2="120" stroke="#000000" stroke-width="1.2"/>
  <line x1="830" y1="420" x2="520" y2="120" stroke="#000000" stroke-width="1.2"/>

  <!-- Include / Extend Relationships (Dashed with arrows) -->
  <!-- UC1 -> UC2 <<include>> -->
  <line x1="430" y1="135" x2="480" y2="150" stroke="#000000" stroke-width="1.2" stroke-dasharray="4,3" marker-end="url(#ucArrow)"/>
  <text x="470" y="138" font-family="'Times New Roman', Times, serif" font-size="8" fill="#000000">&lt;&lt;include&gt;&gt;</text>

  <!-- UC3 -> UC4 <<include>> -->
  <line x1="430" y1="235" x2="480" y2="250" stroke="#000000" stroke-width="1.2" stroke-dasharray="4,3" marker-end="url(#ucArrow)"/>
  <text x="470" y="238" font-family="'Times New Roman', Times, serif" font-size="8" fill="#000000">&lt;&lt;include&gt;&gt;</text>

  <!-- UC5 -> UC6 <<extend>> -->
  <line x1="400" y1="343" x2="400" y2="375" stroke="#000000" stroke-width="1.2" stroke-dasharray="4,3" marker-end="url(#ucArrow)"/>
  <text x="410" y="362" font-family="'Times New Roman', Times, serif" font-size="8" fill="#000000">&lt;&lt;extend&gt;&gt;</text>

  <!-- UC6 -> UC7 <<include>> -->
  <line x1="400" y1="423" x2="400" y2="455" stroke="#000000" stroke-width="1.2" stroke-dasharray="4,3" marker-end="url(#ucArrow)"/>
  <text x="410" y="442" font-family="'Times New Roman', Times, serif" font-size="8" fill="#000000">&lt;&lt;include&gt;&gt;</text>

  <!-- UC7 -> UC8 <<include>> -->
  <line x1="400" y1="503" x2="400" y2="535" stroke="#000000" stroke-width="1.2" stroke-dasharray="4,3" marker-end="url(#ucArrow)"/>
  <text x="410" y="522" font-family="'Times New Roman', Times, serif" font-size="8" fill="#000000">&lt;&lt;include&gt;&gt;</text>
</svg>'''

def get_uml_class_svg():
    return '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 960 760" width="100%" height="auto">
  <defs>
    
    <marker id="generalization" viewBox="0 0 12 12" refX="10" refY="6" markerWidth="8" markerHeight="8" orient="auto">
      <polygon points="0,0 12,6 0,12" fill="#ffffff" stroke="#000000" stroke-width="1.5"/>
    </marker>
    <marker id="association" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto">
      <path d="M 0 2 L 8 5 L 0 8" fill="none" stroke="#000000" stroke-width="1.5"/>
    </marker>
  </defs>

  <rect width="960" height="760" fill="#ffffff" stroke="#000000" stroke-width="1.2"/>

  <!-- Title -->
  <rect x="20" y="15" width="920" height="42" rx="6" fill="#000000" stroke="#000000"/>
  <text x="480" y="41" font-family="'Times New Roman', Times, serif" font-size="14" font-weight="700" fill="#ffffff" text-anchor="middle">
    ALPHATEMPORAL OBJECT-ORIENTED CLASS DIAGRAM (UML 2.5)
  </text>

  <!-- CLASS 1: DataLoader -->
  <g transform="translate(30, 75)">
    <rect width="210" height="150" fill="#ffffff" stroke="#000000" stroke-width="1.2" stroke="#000000" stroke-width="1.2" rx="3"/>
    <rect width="210" height="24" fill="#eeeeee" stroke="#000000" stroke-width="1" rx="0"/>
    <text x="105" y="16" font-family="'Times New Roman', Times, serif" font-size="10" font-weight="700" fill="#000000" text-anchor="middle">DataLoader</text>
    <!-- Attributes -->
    <line x1="0" y1="24" x2="210" y2="24" stroke="#000000" stroke-width="1"/>
    <text x="6" y="38" font-family="'Courier New', Courier, monospace" font-size="8" fill="#000000">- _memory_cache: dict</text>
    <text x="6" y="50" font-family="'Courier New', Courier, monospace" font-size="8" fill="#000000">- _cache_ttl_sec: float = 60.0</text>
    <text x="6" y="62" font-family="'Courier New', Courier, monospace" font-size="8" fill="#000000">- storage_dir: Path</text>
    <!-- Operations -->
    <line x1="0" y1="68" x2="210" y2="68" stroke="#000000" stroke-width="1"/>
    <text x="6" y="82" font-family="'Courier New', Courier, monospace" font-size="8" fill="#000000">+ fetch_live_data(ticker): DataFrame</text>
    <text x="6" y="94" font-family="'Courier New', Courier, monospace" font-size="8" fill="#000000">+ load_sector_data(key): DataFrame</text>
    <text x="6" y="106" font-family="'Courier New', Courier, monospace" font-size="8" fill="#000000">+ save_cache(ticker, df): void</text>
    <text x="6" y="118" font-family="'Courier New', Courier, monospace" font-size="8" fill="#000000">- _build_synthetic_continuum(): DF</text>
    <text x="6" y="130" font-family="'Courier New', Courier, monospace" font-size="8" fill="#000000">+ clear_expired_cache(): int</text>
  </g>

  <!-- CLASS 2: MarketSessionTracker -->
  <g transform="translate(270, 75)">
    <rect width="210" height="150" fill="#ffffff" stroke="#000000" stroke-width="1.2" stroke="#000000" stroke-width="1.2" rx="3"/>
    <rect width="210" height="24" fill="#eeeeee" stroke="#000000" stroke-width="1" rx="0"/>
    <text x="105" y="16" font-family="'Times New Roman', Times, serif" font-size="10" font-weight="700" fill="#000000" text-anchor="middle">MarketSessionTracker</text>
    <line x1="0" y1="24" x2="210" y2="24" stroke="#000000" stroke-width="1"/>
    <text x="6" y="38" font-family="'Courier New', Courier, monospace" font-size="8" fill="#000000">- NSE_OPEN_IST: time = 09:15</text>
    <text x="6" y="50" font-family="'Courier New', Courier, monospace" font-size="8" fill="#000000">- NSE_CLOSE_IST: time = 15:30</text>
    <text x="6" y="62" font-family="'Courier New', Courier, monospace" font-size="8" fill="#000000">- _tz_ist: ZoneInfo</text>
    <line x1="0" y1="68" x2="210" y2="68" stroke="#000000" stroke-width="1"/>
    <text x="6" y="82" font-family="'Courier New', Courier, monospace" font-size="8" fill="#000000">+ is_market_open(ticker): bool</text>
    <text x="6" y="94" font-family="'Courier New', Courier, monospace" font-size="8" fill="#000000">+ get_session_state(ticker): dict</text>
    <text x="6" y="106" font-family="'Courier New', Courier, monospace" font-size="8" fill="#000000">+ enforce_closing_cross(df): DF</text>
    <text x="6" y="118" font-family="'Courier New', Courier, monospace" font-size="8" fill="#000000">+ get_effective_ttl(ticker): float</text>
  </g>

  <!-- CLASS 3: FractionalDifferentiator -->
  <g transform="translate(510, 75)">
    <rect width="210" height="150" fill="#ffffff" stroke="#000000" stroke-width="1.2" stroke="#000000" stroke-width="1.2" rx="3"/>
    <rect width="210" height="24" fill="#eeeeee" stroke="#000000" stroke-width="1" rx="0"/>
    <text x="105" y="16" font-family="'Times New Roman', Times, serif" font-size="10" font-weight="700" fill="#000000" text-anchor="middle">FractionalDifferentiator</text>
    <line x1="0" y1="24" x2="210" y2="24" stroke="#000000" stroke-width="1"/>
    <text x="6" y="38" font-family="'Courier New', Courier, monospace" font-size="8" fill="#000000">- default_threshold: float = 1e-4</text>
    <text x="6" y="50" font-family="'Courier New', Courier, monospace" font-size="8" fill="#000000">- max_lags: int = 1</text>
    <line x1="0" y1="56" x2="210" y2="56" stroke="#000000" stroke-width="1"/>
    <text x="6" y="70" font-family="'Courier New', Courier, monospace" font-size="8" fill="#000000">+ get_memory_weights(d, size): array</text>
    <text x="6" y="82" font-family="'Courier New', Courier, monospace" font-size="8" fill="#000000">+ frac_diff_ffd(series, d): Series</text>
    <text x="6" y="94" font-family="'Courier New', Courier, monospace" font-size="8" fill="#000000">+ find_optimal_d(series): dict</text>
    <text x="6" y="106" font-family="'Courier New', Courier, monospace" font-size="8" fill="#000000">- _run_adf_test(series): float</text>
  </g>

  <!-- CLASS 4: BaseModel (Abstract) -->
  <g transform="translate(750, 75)">
    <rect width="180" height="150" fill="#ffffff" stroke="#000000" stroke-width="1.2" stroke="#000000" stroke-width="1.2" rx="3"/>
    <rect width="180" height="24" fill="#eeeeee" stroke="#000000" stroke-width="1" rx="0"/>
    <text x="90" y="16" font-family="'Times New Roman', Times, serif" font-size="10" font-weight="700" fill="#000000" text-anchor="middle">&lt;&lt;Abstract&gt;&gt; BaseModel</text>
    <line x1="0" y1="24" x2="180" y2="24" stroke="#000000" stroke-width="1"/>
    <text x="6" y="38" font-family="'Courier New', Courier, monospace" font-size="8" fill="#000000"># model_name: str</text>
    <text x="6" y="50" font-family="'Courier New', Courier, monospace" font-size="8" fill="#000000"># is_fitted: bool = False</text>
    <text x="6" y="62" font-family="'Courier New', Courier, monospace" font-size="8" fill="#000000"># device: torch.device</text>
    <line x1="0" y1="68" x2="180" y2="68" stroke="#000000" stroke-width="1"/>
    <text x="6" y="82" font-family="'Courier New', Courier, monospace" font-size="8" fill="#000000">+ fit(X, y): void</text>
    <text x="6" y="94" font-family="'Courier New', Courier, monospace" font-size="8" fill="#000000">+ predict(X): ndarray</text>
    <text x="6" y="106" font-family="'Courier New', Courier, monospace" font-size="8" fill="#000000">+ predict_proba(X): ndarray</text>
    <text x="6" y="118" font-family="'Courier New', Courier, monospace" font-size="8" fill="#000000">+ save_weights(path): void</text>
  </g>

  <!-- CLASS 5: PyTorchTCN (Inherits BaseModel) -->
  <g transform="translate(30, 265)">
    <rect width="210" height="160" fill="#ffffff" stroke="#000000" stroke-width="1.2" rx="3"/>
    <rect width="210" height="24" fill="#eeeeee" stroke="#000000" stroke-width="1" rx="0"/>
    <text x="105" y="16" font-family="'Times New Roman', Times, serif" font-size="10" font-weight="700" fill="#000000" text-anchor="middle">PyTorchTCN</text>
    <line x1="0" y1="24" x2="210" y2="24" stroke="#000000" stroke-width="1"/>
    <text x="6" y="38" font-family="'Courier New', Courier, monospace" font-size="8" fill="#000000">- num_channels: list = [64,64,128,128]</text>
    <text x="6" y="50" font-family="'Courier New', Courier, monospace" font-size="8" fill="#000000">- kernel_size: int = 3</text>
    <text x="6" y="62" font-family="'Courier New', Courier, monospace" font-size="8" fill="#000000">- network: nn.Sequential</text>
    <line x1="0" y1="68" x2="210" y2="68" stroke="#000000" stroke-width="1"/>
    <text x="6" y="82" font-family="'Courier New', Courier, monospace" font-size="8" fill="#000000">+ forward(x: Tensor): Tensor</text>
    <text x="6" y="94" font-family="'Courier New', Courier, monospace" font-size="8" fill="#000000">+ fit(X_seq, y): void</text>
    <text x="6" y="106" font-family="'Courier New', Courier, monospace" font-size="8" fill="#000000">+ predict_proba(X_seq): ndarray</text>
    <text x="6" y="118" font-family="'Courier New', Courier, monospace" font-size="8" fill="#000000">+ get_receptive_field(): int = 61</text>
  </g>

  <!-- CLASS 6: PyTorchTFT (Inherits BaseModel) -->
  <g transform="translate(270, 265)">
    <rect width="210" height="160" fill="#ffffff" stroke="#000000" stroke-width="1.2" rx="3"/>
    <rect width="210" height="24" fill="#eeeeee" stroke="#000000" stroke-width="1" rx="0"/>
    <text x="105" y="16" font-family="'Times New Roman', Times, serif" font-size="10" font-weight="700" fill="#000000" text-anchor="middle">PyTorchTFT</text>
    <line x1="0" y1="24" x2="210" y2="24" stroke="#000000" stroke-width="1"/>
    <text x="6" y="38" font-family="'Courier New', Courier, monospace" font-size="8" fill="#000000">- vsn: VariableSelectionNetwork</text>
    <text x="6" y="50" font-family="'Courier New', Courier, monospace" font-size="8" fill="#000000">- lstm_encoder: nn.LSTM</text>
    <text x="6" y="62" font-family="'Courier New', Courier, monospace" font-size="8" fill="#000000">- self_attn: InterpretableMultiHeadAttn</text>
    <line x1="0" y1="68" x2="210" y2="68" stroke="#000000" stroke-width="1"/>
    <text x="6" y="82" font-family="'Courier New', Courier, monospace" font-size="8" fill="#000000">+ forward(x): (Tensor, Tensor)</text>
    <text x="6" y="94" font-family="'Courier New', Courier, monospace" font-size="8" fill="#000000">+ fit(X_seq, y): void</text>
    <text x="6" y="106" font-family="'Courier New', Courier, monospace" font-size="8" fill="#000000">+ predict_proba(X_seq): ndarray</text>
    <text x="6" y="118" font-family="'Courier New', Courier, monospace" font-size="8" fill="#000000">+ get_feature_importances(): dict</text>
  </g>

  <!-- CLASS 7: StackingMetaEnsemble -->
  <g transform="translate(510, 265)">
    <rect width="210" height="160" fill="#ffffff" stroke="#000000" stroke-width="1.2" rx="3"/>
    <rect width="210" height="24" fill="#eeeeee" stroke="#000000" stroke-width="1" rx="0"/>
    <text x="105" y="16" font-family="'Times New Roman', Times, serif" font-size="10" font-weight="700" fill="#000000" text-anchor="middle">StackingMetaEnsemble</text>
    <line x1="0" y1="24" x2="210" y2="24" stroke="#000000" stroke-width="1"/>
    <text x="6" y="38" font-family="'Courier New', Courier, monospace" font-size="8" fill="#000000">- base_models: dict[str, BaseModel]</text>
    <text x="6" y="50" font-family="'Courier New', Courier, monospace" font-size="8" fill="#000000">- meta_learner: LogisticRegression</text>
    <text x="6" y="62" font-family="'Courier New', Courier, monospace" font-size="8" fill="#000000">- cv_folds: int = 5</text>
    <line x1="0" y1="68" x2="210" y2="68" stroke="#000000" stroke-width="1"/>
    <text x="6" y="82" font-family="'Courier New', Courier, monospace" font-size="8" fill="#000000">+ fit(X, y): void</text>
    <text x="6" y="94" font-family="'Courier New', Courier, monospace" font-size="8" fill="#000000">+ predict_proba(X): ndarray</text>
    <text x="6" y="106" font-family="'Courier New', Courier, monospace" font-size="8" fill="#000000">- _oof_probability_blend(X, y): array</text>
  </g>

  <!-- CLASS 8: ChowSelectiveClassifier -->
  <g transform="translate(750, 265)">
    <rect width="180" height="160" fill="#ffffff" stroke="#000000" stroke-width="1.2" rx="3"/>
    <rect width="180" height="24" fill="#eeeeee" stroke="#000000" stroke-width="1" rx="0"/>
    <text x="90" y="16" font-family="'Times New Roman', Times, serif" font-size="10" font-weight="700" fill="#000000" text-anchor="middle">ChowSelectiveClassifier</text>
    <line x1="0" y1="24" x2="180" y2="24" stroke="#000000" stroke-width="1"/>
    <text x="6" y="38" font-family="'Courier New', Courier, monospace" font-size="8" fill="#000000">- tau: float = 0.75</text>
    <text x="6" y="50" font-family="'Courier New', Courier, monospace" font-size="8" fill="#000000">- base_estimator: BaseModel</text>
    <line x1="0" y1="56" x2="180" y2="56" stroke="#000000" stroke-width="1"/>
    <text x="6" y="70" font-family="'Courier New', Courier, monospace" font-size="8" fill="#000000">+ predict_selective(X): dict</text>
    <text x="6" y="82" font-family="'Courier New', Courier, monospace" font-size="8" fill="#000000">+ compute_coverage(X): float</text>
    <text x="6" y="94" font-family="'Courier New', Courier, monospace" font-size="8" fill="#000000">+ bound_error(tau): float</text>
    <text x="6" y="106" font-family="'Courier New', Courier, monospace" font-size="8" fill="#000000">+ evaluate_walk_forward(): dict</text>
  </g>

  <!-- CLASS 9: MertonCreditRiskSolver -->
  <g transform="translate(30, 465)">
    <rect width="210" height="150" fill="#ffffff" stroke="#000000" stroke-width="1.2" rx="3"/>
    <rect width="210" height="24" fill="#eeeeee" stroke="#000000" stroke-width="1" rx="0"/>
    <text x="105" y="16" font-family="'Times New Roman', Times, serif" font-size="10" font-weight="700" fill="#000000" text-anchor="middle">MertonCreditRiskSolver</text>
    <line x1="0" y1="24" x2="210" y2="24" stroke="#000000" stroke-width="1"/>
    <text x="6" y="38" font-family="'Courier New', Courier, monospace" font-size="8" fill="#000000">- r: float = 0.045</text>
    <text x="6" y="50" font-family="'Courier New', Courier, monospace" font-size="8" fill="#000000">- T: float = 1.0</text>
    <line x1="0" y1="56" x2="210" y2="56" stroke="#000000" stroke-width="1"/>
    <text x="6" y="70" font-family="'Courier New', Courier, monospace" font-size="8" fill="#000000">+ solve(cap, vol, debt): dict</text>
    <text x="6" y="82" font-family="'Courier New', Courier, monospace" font-size="8" fill="#000000">+ compute_altman_z(fundamentals): dict</text>
    <text x="6" y="94" font-family="'Courier New', Courier, monospace" font-size="8" fill="#000000">+ evaluate_veto_rule(z, dd): bool</text>
  </g>

  <!-- CLASS 10: HalfKellyAllocator -->
  <g transform="translate(270, 465)">
    <rect width="210" height="150" fill="#ffffff" stroke="#000000" stroke-width="1.2" rx="3"/>
    <rect width="210" height="24" fill="#eeeeee" stroke="#000000" stroke-width="1" rx="0"/>
    <text x="105" y="16" font-family="'Times New Roman', Times, serif" font-size="10" font-weight="700" fill="#000000" text-anchor="middle">HalfKellyAllocator</text>
    <line x1="0" y1="24" x2="210" y2="24" stroke="#000000" stroke-width="1"/>
    <text x="6" y="38" font-family="'Courier New', Courier, monospace" font-size="8" fill="#000000">- max_cap_pct: float = 0.20</text>
    <text x="6" y="50" font-family="'Courier New', Courier, monospace" font-size="8" fill="#000000">- fraction_multiplier: float = 0.50</text>
    <line x1="0" y1="56" x2="210" y2="56" stroke="#000000" stroke-width="1"/>
    <text x="6" y="70" font-family="'Courier New', Courier, monospace" font-size="8" fill="#000000">+ compute_fraction(p, b, beta): float</text>
    <text x="6" y="82" font-family="'Courier New', Courier, monospace" font-size="8" fill="#000000">+ generate_trade_action_plan(...): dict</text>
  </g>

  <!-- CLASS 11: AdvancedRiskBacktester -->
  <g transform="translate(510, 465)">
    <rect width="210" height="150" fill="#ffffff" stroke="#000000" stroke-width="1.2" rx="3"/>
    <rect width="210" height="24" fill="#eeeeee" stroke="#000000" stroke-width="1" rx="0"/>
    <text x="105" y="16" font-family="'Times New Roman', Times, serif" font-size="10" font-weight="700" fill="#000000" text-anchor="middle">AdvancedRiskBacktester</text>
    <line x1="0" y1="24" x2="210" y2="24" stroke="#000000" stroke-width="1"/>
    <text x="6" y="38" font-family="'Courier New', Courier, monospace" font-size="8" fill="#000000">- initial_capital: float = 100000.0</text>
    <text x="6" y="50" font-family="'Courier New', Courier, monospace" font-size="8" fill="#000000">- slippage_bps: float = 5.0</text>
    <line x1="0" y1="56" x2="210" y2="56" stroke="#000000" stroke-width="1"/>
    <text x="6" y="70" font-family="'Courier New', Courier, monospace" font-size="8" fill="#000000">+ run_triple_barrier_backtest(): dict</text>
    <text x="6" y="82" font-family="'Courier New', Courier, monospace" font-size="8" fill="#000000">+ run_monte_carlo(n_sims=500): dict</text>
  </g>

  <!-- CLASS 12: SystemTelemetry -->
  <g transform="translate(750, 465)">
    <rect width="180" height="150" fill="#ffffff" stroke="#000000" stroke-width="1.2" rx="3"/>
    <rect width="180" height="24" fill="#eeeeee" stroke="#000000" stroke-width="1" rx="0"/>
    <text x="90" y="16" font-family="'Times New Roman', Times, serif" font-size="10" font-weight="700" fill="#000000" text-anchor="middle">SystemTelemetry</text>
    <line x1="0" y1="24" x2="180" y2="24" stroke="#000000" stroke-width="1"/>
    <text x="6" y="38" font-family="'Courier New', Courier, monospace" font-size="8" fill="#000000">- _start_time: float</text>
    <line x1="0" y1="44" x2="180" y2="44" stroke="#000000" stroke-width="1"/>
    <text x="6" y="58" font-family="'Courier New', Courier, monospace" font-size="8" fill="#000000">+ get_gpu_diagnostics(): dict</text>
    <text x="6" y="70" font-family="'Courier New', Courier, monospace" font-size="8" fill="#000000">+ get_host_memory(): dict</text>
    <text x="6" y="82" font-family="'Courier New', Courier, monospace" font-size="8" fill="#000000">+ get_active_models(): list</text>
  </g>

  <!-- Generalization Arrows (BaseModel Inheritance) -->
  <line x1="135" y1="265" x2="790" y2="225" stroke="#000000" stroke-width="1.2" marker-end="url(#generalization)"/>
  <line x1="375" y1="265" x2="810" y2="225" stroke="#000000" stroke-width="1.2" marker-end="url(#generalization)"/>
  <line x1="615" y1="265" x2="830" y2="225" stroke="#000000" stroke-width="1.2" marker-end="url(#generalization)"/>

  <!-- Associations -->
  <line x1="240" y1="150" x2="270" y2="150" stroke="#000000" stroke-width="1.2" marker-end="url(#association)"/>
  <line x1="720" y1="345" x2="750" y2="345" stroke="#000000" stroke-width="1.2" marker-end="url(#association)"/>
  <line x1="240" y1="540" x2="270" y2="540" stroke="#000000" stroke-width="1.2" marker-end="url(#association)"/>
</svg>'''

def get_uml_sequence_svg():
    return '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 960 740" width="100%" height="auto">
  <defs>
    
    <marker id="seqArrow" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto">
      <path d="M 0 1 L 10 5 L 0 9 z" fill="#000000"/>
    </marker>
    <marker id="seqReturn" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto">
      <path d="M 0 1 L 10 5 L 0 9 z" fill="#000000"/>
    </marker>
  </defs>

  <rect width="960" height="740" fill="#ffffff" stroke="#000000" stroke-width="1.2"/>

  <!-- Header -->
  <rect x="20" y="15" width="920" height="42" rx="6" fill="#000000" stroke="#000000"/>
  <text x="480" y="41" font-family="'Times New Roman', Times, serif" font-size="14" font-weight="700" fill="#ffffff" text-anchor="middle">
    UML SEQUENCE DIAGRAM: END-TO-END INSTITUTIONAL PREDICTION LIFECYCLE
  </text>

  <!-- Lifelines -->
  <!-- 1. Client -->
  <g transform="translate(40, 75)">
    <rect width="100" height="34" rx="4" fill="#ffffff" stroke="#000000" stroke-width="1.2"/>
    <text x="50" y="21" font-family="'Times New Roman', Times, serif" font-size="10" font-weight="700" fill="#000000" text-anchor="middle">:TraderClient</text>
    <line x1="50" y1="34" x2="50" y2="630" stroke="#000000" stroke-width="1.2" stroke-dasharray="5,4"/>
  </g>

  <!-- 2. FastAPI Gateway -->
  <g transform="translate(180, 75)">
    <rect width="110" height="34" rx="4" fill="#ffffff" stroke="#000000" stroke-width="1.2"/>
    <text x="55" y="21" font-family="'Times New Roman', Times, serif" font-size="10" font-weight="700" fill="#000000" text-anchor="middle">:FastAPIGateway</text>
    <line x1="55" y1="34" x2="55" y2="630" stroke="#000000" stroke-width="1.2" stroke-dasharray="5,4"/>
  </g>

  <!-- 3. DataLoader & SessionLock -->
  <g transform="translate(330, 75)">
    <rect width="115" height="34" rx="4" fill="#ffffff" stroke="#000000" stroke-width="1.2"/>
    <text x="57" y="21" font-family="'Times New Roman', Times, serif" font-size="10" font-weight="700" fill="#000000" text-anchor="middle">:SessionDataLoader</text>
    <line x1="57" y1="34" x2="57" y2="630" stroke="#000000" stroke-width="1.2" stroke-dasharray="5,4"/>
  </g>

  <!-- 4. FeatureEngine (HMA & FracDiff) -->
  <g transform="translate(480, 75)">
    <rect width="115" height="34" rx="4" fill="#ffffff" stroke="#000000" stroke-width="1.2"/>
    <text x="57" y="21" font-family="'Times New Roman', Times, serif" font-size="10" font-weight="700" fill="#000000" text-anchor="middle">:VectorizedEngine</text>
    <line x1="57" y1="34" x2="57" y2="630" stroke="#000000" stroke-width="1.2" stroke-dasharray="5,4"/>
  </g>

  <!-- 5. TemporalEnsemble (CUDA) -->
  <g transform="translate(630, 75)">
    <rect width="120" height="34" rx="4" fill="#ffffff" stroke="#000000" stroke-width="1.2"/>
    <text x="60" y="21" font-family="'Times New Roman', Times, serif" font-size="10" font-weight="700" fill="#000000" text-anchor="middle">:TemporalEnsemble</text>
    <line x1="60" y1="34" x2="60" y2="630" stroke="#000000" stroke-width="1.2" stroke-dasharray="5,4"/>
  </g>

  <!-- 6. Chow & Risk Engine -->
  <g transform="translate(790, 75)">
    <rect width="130" height="34" rx="4" fill="#ffffff" stroke="#000000" stroke-width="1.2"/>
    <text x="65" y="21" font-family="'Times New Roman', Times, serif" font-size="10" font-weight="700" fill="#000000" text-anchor="middle">:RiskGatingEngine</text>
    <line x1="65" y1="34" x2="65" y2="630" stroke="#000000" stroke-width="1.2" stroke-dasharray="5,4"/>
  </g>

  <!-- Activation Bars -->
  <rect x="85" y="125" width="10" height="490" fill="#f4f4f4" stroke="#000000" stroke-width="1"/>
  <rect x="230" y="130" width="10" height="480" fill="#f4f4f4" stroke="#000000" stroke-width="1"/>
  <rect x="382" y="145" width="10" height="75" fill="#f4f4f4" stroke="#000000" stroke-width="1"/>
  <rect x="532" y="235" width="10" height="75" fill="#f4f4f4" stroke="#000000" stroke-width="1"/>
  <rect x="685" y="325" width="10" height="70" fill="#f4f4f4" stroke="#000000" stroke-width="1"/>
  <rect x="850" y="410" width="10" height="150" fill="#f4f4f4" stroke="#000000" stroke-width="1"/>

  <!-- Sequence Calls -->
  <!-- 1. POST /api/predict -->
  <line x1="95" y1="135" x2="228" y2="135" stroke="#000000" stroke-width="1.5" marker-end="url(#seqArrow)"/>
  <text x="160" y="128" font-family="'Courier New', Courier, monospace" font-size="8" fill="#000000" text-anchor="middle">1: POST /api/predict (ticker="TCS.NS")</text>

  <!-- 2. fetch_live_data() -->
  <line x1="240" y1="150" x2="380" y2="150" stroke="#000000" stroke-width="1.5" marker-end="url(#seqArrow)"/>
  <text x="310" y="144" font-family="'Courier New', Courier, monospace" font-size="8" fill="#000000" text-anchor="middle">2: fetch_live_data()</text>

  <!-- 3. Self Call: enforce_closing_cross() -->
  <path d="M 392 165 C 430 165 430 185 392 185" fill="none" stroke="#000000" stroke-width="1.2" marker-end="url(#seqArrow)"/>
  <text x="440" y="178" font-family="'Courier New', Courier, monospace" font-size="8" fill="#000000">2.1: enforce_session_lock(09:15-15:30 IST)</text>

  <!-- Return Raw Data -->
  <line x1="380" y1="215" x2="242" y2="215" stroke="#000000" stroke-width="1.2" stroke-dasharray="4,3" marker-end="url(#seqReturn)"/>
  <text x="310" y="208" font-family="'Courier New', Courier, monospace" font-size="8" fill="#000000" text-anchor="middle">clean_df (OHLCV)</text>

  <!-- 4. compute_26_indicators() & frac_diff() -->
  <line x1="240" y1="240" x2="530" y2="240" stroke="#000000" stroke-width="1.5" marker-end="url(#seqArrow)"/>
  <text x="385" y="234" font-family="'Courier New', Courier, monospace" font-size="8" fill="#000000" text-anchor="middle">3: compute_full_quant_features(clean_df)</text>

  <!-- Self Call: 1D FIR Convolution -->
  <path d="M 542 255 C 580 255 580 275 542 275" fill="none" stroke="#000000" stroke-width="1.2" marker-end="url(#seqArrow)"/>
  <text x="590" y="268" font-family="'Courier New', Courier, monospace" font-size="8" fill="#000000">3.1: 1D FIR HMA Convolution (AVX-256)</text>

  <!-- Return Feature Tensor -->
  <line x1="530" y1="305" x2="242" y2="305" stroke="#000000" stroke-width="1.2" stroke-dasharray="4,3" marker-end="url(#seqReturn)"/>
  <text x="385" y="298" font-family="'Courier New', Courier, monospace" font-size="8" fill="#000000" text-anchor="middle">feature_tensor (Batch, 20, 26)</text>

  <!-- 5. Forward Pass on GPU -->
  <line x1="240" y1="330" x2="683" y2="330" stroke="#000000" stroke-width="1.5" marker-end="url(#seqArrow)"/>
  <text x="460" y="324" font-family="'Courier New', Courier, monospace" font-size="8" fill="#000000" text-anchor="middle">4: forward(tensor.to("cuda")) [TCN + TFT + BiLSTM]</text>

  <!-- Return Raw Posteriors -->
  <line x1="683" y1="390" x2="242" y2="390" stroke="#000000" stroke-width="1.2" stroke-dasharray="4,3" marker-end="url(#seqReturn)"/>
  <text x="460" y="383" font-family="'Courier New', Courier, monospace" font-size="8" fill="#000000" text-anchor="middle">posterior_probabilities [P(Up)=0.88, P(Down)=0.12]</text>

  <!-- 6. Evaluate Chow Rule & Credit Risk -->
  <line x1="240" y1="415" x2="848" y2="415" stroke="#000000" stroke-width="1.5" marker-end="url(#seqArrow)"/>
  <text x="540" y="409" font-family="'Courier New', Courier, monospace" font-size="8" fill="#000000" text-anchor="middle">5: evaluate_trade(posteriors, ticker)</text>

  <!-- ALT FRAME: Chow Confidence & Risk Veto -->
  <rect x="220" y="435" width="670" height="135" fill="#ffffff" stroke="#000000" stroke-width="1" stroke-dasharray="5,3"/>
  <rect x="220" y="435" width="70" height="18" fill="#000000"/>
  <text x="255" y="448" font-family="'Times New Roman', Times, serif" font-size="8" font-weight="700" fill="#ffffff" text-anchor="middle">alt [tau &ge; 0.75]</text>

  <line x1="850" y1="460" x2="242" y2="460" stroke="#000000" stroke-width="1.2" stroke-dasharray="4,3" marker-end="url(#seqReturn)"/>
  <text x="540" y="454" font-family="'Courier New', Courier, monospace" font-size="8" fill="#000000" text-anchor="middle">[CONFIRMED TRADE]: Merton Safe (DD=4.2), Altman Z=3.14 &rarr; Half-Kelly Sized (12.4%)</text>

  <!-- Dividing Line in Alt -->
  <line x1="220" y1="495" x2="890" y2="495" stroke="#000000" stroke-width="1" stroke-dasharray="4,4"/>
  <text x="255" y="510" font-family="'Times New Roman', Times, serif" font-size="8" font-weight="700" fill="#333333" text-anchor="middle">[else: tau &lt; 0.75]</text>

  <line x1="850" y1="535" x2="242" y2="535" stroke="#000000" stroke-width="1.2" stroke-dasharray="4,3" marker-end="url(#seqReturn)"/>
  <text x="540" y="528" font-family="'Courier New', Courier, monospace" font-size="8" fill="#000000" text-anchor="middle">[ABSTAIN / CASH]: Sideways chop regime &rarr; Zero execution risk bounded</text>

  <!-- Final HTTP JSON Response -->
  <line x1="230" y1="590" x2="95" y2="590" stroke="#000000" stroke-width="1.5" stroke-dasharray="4,3" marker-end="url(#seqReturn)"/>
  <text x="160" y="583" font-family="'Courier New', Courier, monospace" font-size="8" fill="#000000" text-anchor="middle">6: 200 OK (JSON Trade Action Plan)</text>
</svg>'''

def get_uml_collaboration_svg():
    return '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 960 680" width="100%" height="auto">
  <defs>
    
    <marker id="msgArrow" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto">
      <path d="M 0 1 L 10 5 L 0 9 z" fill="#000000"/>
    </marker>
  </defs>

  <rect width="960" height="680" fill="#ffffff" stroke="#000000" stroke-width="1.2"/>

  <!-- Title -->
  <rect x="20" y="15" width="920" height="42" rx="6" fill="#000000" stroke="#000000"/>
  <text x="480" y="41" font-family="'Times New Roman', Times, serif" font-size="14" font-weight="700" fill="#ffffff" text-anchor="middle">
    UML COLLABORATION / COMMUNICATION DIAGRAM (OBJECT MESSAGE TOPOLOGY)
  </text>

  <!-- OBJECT 1: UI / Client -->
  <g transform="translate(60, 100)">
    <rect width="160" height="60" rx="4" fill="#ffffff" stroke="#000000" stroke-width="1.5"/>
    <text x="80" y="26" font-family="'Times New Roman', Times, serif" font-size="10" font-weight="700" fill="#000000" text-anchor="middle">client : WebDashboard</text>
    <text x="80" y="44" font-family="'Times New Roman', Times, serif" font-size="8" fill="#333333" text-anchor="middle">Port 8050 / Port 7860</text>
  </g>

  <!-- OBJECT 2: FastAPI Gateway -->
  <g transform="translate(390, 100)">
    <rect width="180" height="60" rx="4" fill="#ffffff" stroke="#000000" stroke-width="1.5"/>
    <text x="90" y="26" font-family="'Times New Roman', Times, serif" font-size="10" font-weight="700" fill="#000000" text-anchor="middle">gateway : APIGateway</text>
    <text x="90" y="44" font-family="'Times New Roman', Times, serif" font-size="8" fill="#333333" text-anchor="middle">FastAPI Orchestrator</text>
  </g>

  <!-- OBJECT 3: DataLoader & SessionLock -->
  <g transform="translate(720, 100)">
    <rect width="180" height="60" rx="4" fill="#ffffff" stroke="#000000" stroke-width="1.5"/>
    <text x="90" y="26" font-family="'Times New Roman', Times, serif" font-size="10" font-weight="700" fill="#000000" text-anchor="middle">loader : DataLoader</text>
    <text x="90" y="44" font-family="'Times New Roman', Times, serif" font-size="8" fill="#333333" text-anchor="middle">NSE Session Lock (09:15-15:30)</text>
  </g>

  <!-- OBJECT 4: VectorizedEngine -->
  <g transform="translate(720, 310)">
    <rect width="180" height="60" rx="4" fill="#ffffff" stroke="#000000" stroke-width="1.5"/>
    <text x="90" y="26" font-family="'Times New Roman', Times, serif" font-size="10" font-weight="700" fill="#000000" text-anchor="middle">featEngine : Indicators</text>
    <text x="90" y="44" font-family="'Times New Roman', Times, serif" font-size="8" fill="#333333" text-anchor="middle">1D FIR HMA &amp; FracDiff d*</text>
  </g>

  <!-- OBJECT 5: TemporalEnsemble (CUDA) -->
  <g transform="translate(390, 310)">
    <rect width="180" height="60" rx="4" fill="#ffffff" stroke="#000000" stroke-width="1.5"/>
    <text x="90" y="26" font-family="'Times New Roman', Times, serif" font-size="10" font-weight="700" fill="#000000" text-anchor="middle">ensemble : DeepLearning</text>
    <text x="90" y="44" font-family="'Times New Roman', Times, serif" font-size="8" fill="#333333" text-anchor="middle">RTX 3070 Ti CUDA Device</text>
  </g>

  <!-- OBJECT 6: Risk & Allocation Engine -->
  <g transform="translate(60, 310)">
    <rect width="160" height="60" rx="4" fill="#ffffff" stroke="#000000" stroke-width="1.5"/>
    <text x="80" y="26" font-family="'Times New Roman', Times, serif" font-size="10" font-weight="700" fill="#000000" text-anchor="middle">riskEngine : RiskGating</text>
    <text x="80" y="44" font-family="'Times New Roman', Times, serif" font-size="8" fill="#333333" text-anchor="middle">Chow &tau;&ge;0.75 + Merton + Kelly</text>
  </g>

  <!-- OBJECT 7: Telemetry Monitor -->
  <g transform="translate(390, 520)">
    <rect width="180" height="60" rx="4" fill="#ffffff" stroke="#000000" stroke-width="1.5"/>
    <text x="90" y="26" font-family="'Times New Roman', Times, serif" font-size="10" font-weight="700" fill="#000000" text-anchor="middle">telemetry : SystemMonitor</text>
    <text x="90" y="44" font-family="'Times New Roman', Times, serif" font-size="8" fill="#333333" text-anchor="middle">GPU VRAM &amp; Process Telemetry</text>
  </g>

  <!-- Communication Links (Solid Lines between Objects) -->
  <!-- Link 1: client <-> gateway -->
  <line x1="220" y1="130" x2="390" y2="130" stroke="#000000" stroke-width="1.5"/>
  <text x="305" y="118" font-family="'Times New Roman', Times, serif" font-size="8" font-weight="600" fill="#000000">1: predict(ticker) &rarr;</text>
  <text x="305" y="145" font-family="'Times New Roman', Times, serif" font-size="8" font-weight="600" fill="#000000">&larr; 6: return(actionPlan)</text>

  <!-- Link 2: gateway <-> loader -->
  <line x1="570" y1="130" x2="720" y2="130" stroke="#000000" stroke-width="1.5"/>
  <text x="645" y="118" font-family="'Times New Roman', Times, serif" font-size="8" font-weight="600" fill="#000000">2: fetch(ticker) &rarr;</text>
  <text x="645" y="145" font-family="'Times New Roman', Times, serif" font-size="8" font-weight="600" fill="#000000">&larr; 2.1: cleanDF</text>

  <!-- Link 3: loader <-> featEngine -->
  <line x1="810" y1="160" x2="810" y2="310" stroke="#000000" stroke-width="1.5"/>
  <text x="820" y="235" font-family="'Times New Roman', Times, serif" font-size="8" font-weight="600" fill="#000000">3: vectorize(cleanDF) &darr;</text>

  <!-- Link 4: featEngine <-> ensemble -->
  <line x1="720" y1="340" x2="570" y2="340" stroke="#000000" stroke-width="1.5"/>
  <text x="645" y="332" font-family="'Times New Roman', Times, serif" font-size="8" font-weight="600" fill="#000000">&larr; 4: infer(featureTensor)</text>

  <!-- Link 5: ensemble <-> riskEngine -->
  <line x1="390" y1="340" x2="220" y2="340" stroke="#000000" stroke-width="1.5"/>
  <text x="305" y="332" font-family="'Times New Roman', Times, serif" font-size="8" font-weight="600" fill="#000000">&larr; 5: evaluate(posteriors)</text>

  <!-- Link 6: riskEngine <-> client (Diagonal) -->
  <line x1="140" y1="310" x2="140" y2="160" stroke="#000000" stroke-width="1.5"/>
  <text x="145" y="235" font-family="'Times New Roman', Times, serif" font-size="8" font-weight="600" fill="#000000">&uarr; 5.1: updateExecution()</text>

  <!-- Link 7: gateway <-> telemetry -->
  <line x1="480" y1="160" x2="480" y2="520" stroke="#000000" stroke-width="1.5"/>
  <text x="490" y="440" font-family="'Times New Roman', Times, serif" font-size="8" font-weight="600" fill="#000000">7: queryHealth() &darr;</text>
</svg>'''

def get_uml_activity_svg():
    return '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 960 760" width="100%" height="auto">
  <defs>
    
    <marker id="actArrow" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto">
      <path d="M 0 1 L 10 5 L 0 9 z" fill="#000000"/>
    </marker>
  </defs>

  <rect width="960" height="760" fill="#ffffff" stroke="#000000" stroke-width="1.2"/>

  <!-- Title -->
  <rect x="20" y="15" width="920" height="42" rx="6" fill="#000000" stroke="#000000"/>
  <text x="480" y="41" font-family="'Times New Roman', Times, serif" font-size="14" font-weight="700" fill="#ffffff" text-anchor="middle">
    UML ACTIVITY DIAGRAM: INSTITUTIONAL INFERENCE &amp; EXECUTION CONTROL FLOW
  </text>

  <!-- Start Node -->
  <circle cx="480" cy="85" r="12" fill="#000000" stroke="#000000"/>

  <!-- Transition 1 -->
  <line x1="480" y1="97" x2="480" y2="120" stroke="#000000" stroke-width="1.5" marker-end="url(#actArrow)"/>

  <!-- Activity 1: Receive Prediction Request -->
  <rect x="360" y="120" width="240" height="34" rx="17" fill="#ffffff" stroke="#000000" stroke-width="1.5"/>
  <text x="480" y="141" font-family="'Times New Roman', Times, serif" font-size="10" font-weight="600" fill="#000000" text-anchor="middle">Receive Prediction Request (Ticker, Horizon)</text>

  <!-- Transition 2 -->
  <line x1="480" y1="154" x2="480" y2="180" stroke="#000000" stroke-width="1.5" marker-end="url(#actArrow)"/>

  <!-- Activity 2: Check Exchange Session Lock -->
  <rect x="360" y="180" width="240" height="34" rx="17" fill="#ffffff" stroke="#000000" stroke-width="1.5"/>
  <text x="480" y="201" font-family="'Times New Roman', Times, serif" font-size="10" font-weight="600" fill="#000000" text-anchor="middle">Enforce NSE / Binance Session Locking</text>

  <!-- Transition 3: To Fork Bar -->
  <line x1="480" y1="214" x2="480" y2="240" stroke="#000000" stroke-width="1.5" marker-end="url(#actArrow)"/>

  <!-- FORK BAR (Parallel Execution) -->
  <rect x="260" y="240" width="440" height="6" fill="#000000" rx="2"/>

  <!-- Parallel Branch Left: Feature Extraction -->
  <line x1="360" y1="246" x2="360" y2="275" stroke="#000000" stroke-width="1.5" marker-end="url(#actArrow)"/>
  <rect x="250" y="275" width="220" height="38" rx="19" fill="#ffffff" stroke="#000000" stroke-width="1.5"/>
  <text x="360" y="294" font-family="'Times New Roman', Times, serif" font-size="9" font-weight="600" fill="#000000" text-anchor="middle">1D FIR Vectorized HMA &amp; 26 Features</text>
  <text x="360" y="306" font-family="'Times New Roman', Times, serif" font-size="8" fill="#333333" text-anchor="middle">AVX-256 SIMD Parallelization</text>

  <!-- Parallel Branch Right: Fractional Differentiation & Credit Risk -->
  <line x1="600" y1="246" x2="600" y2="275" stroke="#000000" stroke-width="1.5" marker-end="url(#actArrow)"/>
  <rect x="490" y="275" width="220" height="38" rx="19" fill="#ffffff" stroke="#000000" stroke-width="1.5"/>
  <text x="600" y="294" font-family="'Times New Roman', Times, serif" font-size="9" font-weight="600" fill="#000000" text-anchor="middle">Merton DD &amp; Altman Z-Score Solver</text>
  <text x="600" y="306" font-family="'Times New Roman', Times, serif" font-size="8" fill="#333333" text-anchor="middle">Corporate Distress Screening</text>

  <!-- Transitions to JOIN BAR -->
  <line x1="360" y1="313" x2="360" y2="345" stroke="#000000" stroke-width="1.5" marker-end="url(#actArrow)"/>
  <line x1="600" y1="313" x2="600" y2="345" stroke="#000000" stroke-width="1.5" marker-end="url(#actArrow)"/>

  <!-- JOIN BAR -->
  <rect x="260" y="345" width="440" height="6" fill="#000000" rx="2"/>

  <!-- Transition 4: To Neural Ensemble -->
  <line x1="480" y1="351" x2="480" y2="375" stroke="#000000" stroke-width="1.5" marker-end="url(#actArrow)"/>

  <!-- Activity 3: Deep Learning GPU Inference -->
  <rect x="340" y="375" width="280" height="38" rx="19" fill="#ffffff" stroke="#000000" stroke-width="1.5"/>
  <text x="480" y="394" font-family="'Times New Roman', Times, serif" font-size="10" font-weight="600" fill="#000000" text-anchor="middle">Run Temporal Ensemble (TCN + TFT + BiLSTM)</text>
  <text x="480" y="406" font-family="'Times New Roman', Times, serif" font-size="8" fill="#333333" text-anchor="middle">Executed on NVIDIA GeForce RTX 3070 Ti CUDA</text>

  <!-- Transition 5: To Chow Decision Node -->
  <line x1="480" y1="413" x2="480" y2="445" stroke="#000000" stroke-width="1.5" marker-end="url(#actArrow)"/>

  <!-- DECISION NODE 1: Chow Confidence Gate -->
  <polygon points="480,445 520,470 480,495 440,470" fill="#ffffff" stroke="#000000" stroke-width="1.5"/>
  <text x="480" y="473" font-family="'Times New Roman', Times, serif" font-size="8" font-weight="700" fill="#000000" text-anchor="middle">P(max) &ge; 0.75?</text>

  <!-- Branch No (Abstain) -->
  <line x1="520" y1="470" x2="720" y2="470" stroke="#000000" stroke-width="1.5" marker-end="url(#actArrow)"/>
  <text x="590" y="463" font-family="'Times New Roman', Times, serif" font-size="8" font-weight="600" fill="#000000">[No: Chop Noise]</text>
  <rect x="720" y="453" width="180" height="34" rx="17" fill="#ffffff" stroke="#000000" stroke-width="1.5"/>
  <text x="810" y="474" font-family="'Times New Roman', Times, serif" font-size="9" font-weight="600" fill="#000000" text-anchor="middle">Abstain (Hold 100% Cash)</text>

  <!-- Branch Yes (Proceed to Credit Risk Gate) -->
  <line x1="480" y1="495" x2="480" y2="530" stroke="#000000" stroke-width="1.5" marker-end="url(#actArrow)"/>
  <text x="488" y="515" font-family="'Times New Roman', Times, serif" font-size="8" font-weight="600" fill="#000000">[Yes: High Conviction]</text>

  <!-- DECISION NODE 2: Distress Veto Gate -->
  <polygon points="480,530 520,555 480,580 440,555" fill="#ffffff" stroke="#000000" stroke-width="1.5"/>
  <text x="480" y="558" font-family="'Times New Roman', Times, serif" font-size="8" font-weight="700" fill="#000000" text-anchor="middle">Z &lt; 1.81 or DD &lt; 1.5?</text>

  <!-- Branch Yes to Distress (Veto) -->
  <line x1="520" y1="555" x2="720" y2="555" stroke="#000000" stroke-width="1.5" marker-end="url(#actArrow)"/>
  <text x="590" y="548" font-family="'Times New Roman', Times, serif" font-size="8" font-weight="600" fill="#000000">[Yes: Distress Veto]</text>
  <rect x="720" y="538" width="180" height="34" rx="17" fill="#ffffff" stroke="#000000" stroke-width="1.5"/>
  <text x="810" y="559" font-family="'Times New Roman', Times, serif" font-size="9" font-weight="600" fill="#000000" text-anchor="middle">Halt Execution (Distress Veto)</text>

  <!-- Branch No (Safe to Size) -->
  <line x1="480" y1="580" x2="480" y2="615" stroke="#000000" stroke-width="1.5" marker-end="url(#actArrow)"/>
  <text x="488" y="600" font-family="'Times New Roman', Times, serif" font-size="8" font-weight="600" fill="#000000">[No: Prime / Safe]</text>

  <!-- Activity 4: Half-Kelly Sizing & Action Plan -->
  <rect x="350" y="615" width="260" height="36" rx="18" fill="#ffffff" stroke="#000000" stroke-width="1.5"/>
  <text x="480" y="634" font-family="'Times New Roman', Times, serif" font-size="10" font-weight="600" fill="#000000" text-anchor="middle">Generate Half-Kelly Sized Action Plan</text>
  <text x="480" y="646" font-family="'Times New Roman', Times, serif" font-size="8" fill="#333333" text-anchor="middle">Entry, Stop Loss, ATR Trailing Take Profit</text>

  <!-- Terminal Merge -->
  <line x1="480" y1="651" x2="480" y2="690" stroke="#000000" stroke-width="1.5" marker-end="url(#actArrow)"/>
  <line x1="810" y1="487" x2="810" y2="705" stroke="#000000" stroke-width="1.2"/>
  <line x1="810" y1="572" x2="810" y2="705" stroke="#000000" stroke-width="1.2"/>
  <line x1="810" y1="705" x2="495" y2="705" stroke="#000000" stroke-width="1.2" marker-end="url(#actArrow)"/>

  <!-- End Node (Bullseye) -->
  <g transform="translate(480, 705)">
    <circle cx="0" cy="0" r="14" fill="#ffffff" stroke="#000000" stroke-width="2"/>
    <circle cx="0" cy="0" r="8" fill="#000000" stroke="#000000"/>
  </g>
</svg>'''

def get_uml_component_svg():
    return '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 960 700" width="100%" height="auto">
  <defs>
    
    <marker id="compArrow" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto">
      <path d="M 0 1 L 10 5 L 0 9 z" fill="#000000"/>
    </marker>
  </defs>

  <rect width="960" height="700" fill="#ffffff" stroke="#000000" stroke-width="1.2"/>

  <!-- Title -->
  <rect x="20" y="15" width="920" height="42" rx="6" fill="#000000" stroke="#000000"/>
  <text x="480" y="41" font-family="'Times New Roman', Times, serif" font-size="14" font-weight="700" fill="#ffffff" text-anchor="middle">
    UML COMPONENT DIAGRAM: MODULAR SUBSYSTEM INTERFACES &amp; DEPENDENCIES
  </text>

  <!-- Helper macro for component box -->
  <!-- COMPONENT 1: ui_terminal (stock_predict.ui) -->
  <g transform="translate(40, 90)">
    <rect width="240" height="110" rx="4" fill="#ffffff" stroke="#000000" stroke-width="1.5"/>
    <rect x="-8" y="16" width="16" height="10" fill="#ffffff" stroke="#000000" stroke-width="1.2"/>
    <rect x="-8" y="36" width="16" height="10" fill="#ffffff" stroke="#000000" stroke-width="1.2"/>
    <text x="120" y="30" font-family="'Times New Roman', Times, serif" font-size="11" font-weight="700" fill="#000000" text-anchor="middle">&lt;&lt;component&gt;&gt;</text>
    <text x="120" y="48" font-family="'Times New Roman', Times, serif" font-size="11" font-weight="700" fill="#000000" text-anchor="middle">UserInterfaceSubsystem</text>
    <text x="120" y="70" font-family="'Times New Roman', Times, serif" font-size="9" fill="#333333" text-anchor="middle">&bull; GradioApp (7 Tabs)</text>
    <text x="120" y="85" font-family="'Times New Roman', Times, serif" font-size="9" fill="#333333" text-anchor="middle">&bull; TradingView Static Dashboard</text>
  </g>

  <!-- COMPONENT 2: api_gateway (stock_predict.api) -->
  <g transform="translate(360, 90)">
    <rect width="250" height="110" rx="4" fill="#ffffff" stroke="#000000" stroke-width="1.5"/>
    <rect x="-8" y="16" width="16" height="10" fill="#ffffff" stroke="#000000" stroke-width="1.2"/>
    <rect x="-8" y="36" width="16" height="10" fill="#ffffff" stroke="#000000" stroke-width="1.2"/>
    <text x="125" y="30" font-family="'Times New Roman', Times, serif" font-size="11" font-weight="700" fill="#000000" text-anchor="middle">&lt;&lt;component&gt;&gt;</text>
    <text x="125" y="48" font-family="'Times New Roman', Times, serif" font-size="11" font-weight="700" fill="#000000" text-anchor="middle">APIGatewayService</text>
    <text x="125" y="70" font-family="'Times New Roman', Times, serif" font-size="9" fill="#333333" text-anchor="middle">&bull; FastAPI REST Endpoints</text>
    <text x="125" y="85" font-family="'Times New Roman', Times, serif" font-size="9" fill="#333333" text-anchor="middle">&bull; WebSocket OrderBook Streaming</text>
  </g>

  <!-- COMPONENT 3: data_ingestion (stock_predict.data) -->
  <g transform="translate(680, 90)">
    <rect width="240" height="110" rx="4" fill="#ffffff" stroke="#000000" stroke-width="1.5"/>
    <rect x="-8" y="16" width="16" height="10" fill="#ffffff" stroke="#000000" stroke-width="1.2"/>
    <rect x="-8" y="36" width="16" height="10" fill="#ffffff" stroke="#000000" stroke-width="1.2"/>
    <text x="120" y="30" font-family="'Times New Roman', Times, serif" font-size="11" font-weight="700" fill="#000000" text-anchor="middle">&lt;&lt;component&gt;&gt;</text>
    <text x="120" y="48" font-family="'Times New Roman', Times, serif" font-size="11" font-weight="700" fill="#000000" text-anchor="middle">DataIngestionService</text>
    <text x="120" y="70" font-family="'Times New Roman', Times, serif" font-size="9" fill="#333333" text-anchor="middle">&bull; DataLoader &amp; TTL Cache</text>
    <text x="120" y="85" font-family="'Times New Roman', Times, serif" font-size="9" fill="#333333" text-anchor="middle">&bull; MarketSessionTracker</text>
  </g>

  <!-- COMPONENT 4: feature_engine (stock_predict.core) -->
  <g transform="translate(680, 290)">
    <rect width="240" height="120" rx="4" fill="#ffffff" stroke="#000000" stroke-width="1.5"/>
    <rect x="-8" y="16" width="16" height="10" fill="#ffffff" stroke="#000000" stroke-width="1.2"/>
    <rect x="-8" y="36" width="16" height="10" fill="#ffffff" stroke="#000000" stroke-width="1.2"/>
    <text x="120" y="30" font-family="'Times New Roman', Times, serif" font-size="11" font-weight="700" fill="#000000" text-anchor="middle">&lt;&lt;component&gt;&gt;</text>
    <text x="120" y="48" font-family="'Times New Roman', Times, serif" font-size="11" font-weight="700" fill="#000000" text-anchor="middle">SignalEngineeringEngine</text>
    <text x="120" y="70" font-family="'Times New Roman', Times, serif" font-size="9" fill="#333333" text-anchor="middle">&bull; 1D FIR HMA 9 Kernel (AVX-256)</text>
    <text x="120" y="85" font-family="'Times New Roman', Times, serif" font-size="9" fill="#333333" text-anchor="middle">&bull; SuperTrend (28.8x fast)</text>
    <text x="120" y="100" font-family="'Times New Roman', Times, serif" font-size="9" fill="#333333" text-anchor="middle">&bull; FractionalDifferentiator (d*)</text>
  </g>

  <!-- COMPONENT 5: deep_learning_models (stock_predict.models) -->
  <g transform="translate(360, 290)">
    <rect width="250" height="120" rx="4" fill="#ffffff" stroke="#000000" stroke-width="1.5"/>
    <rect x="-8" y="16" width="16" height="10" fill="#ffffff" stroke="#000000" stroke-width="1.2"/>
    <rect x="-8" y="36" width="16" height="10" fill="#ffffff" stroke="#000000" stroke-width="1.2"/>
    <text x="125" y="30" font-family="'Times New Roman', Times, serif" font-size="11" font-weight="700" fill="#000000" text-anchor="middle">&lt;&lt;component&gt;&gt;</text>
    <text x="125" y="48" font-family="'Times New Roman', Times, serif" font-size="11" font-weight="700" fill="#000000" text-anchor="middle">DeepLearningInference</text>
    <text x="125" y="70" font-family="'Times New Roman', Times, serif" font-size="9" fill="#333333" text-anchor="middle">&bull; PyTorchTCN (RF=61, Chomp1d)</text>
    <text x="125" y="85" font-family="'Times New Roman', Times, serif" font-size="9" fill="#333333" text-anchor="middle">&bull; PyTorchTFT (VSN + GRN + Attn)</text>
    <text x="125" y="100" font-family="'Times New Roman', Times, serif" font-size="9" fill="#333333" text-anchor="middle">&bull; BiLSTM with Bahdanau Attention</text>
  </g>

  <!-- COMPONENT 6: ml_stacking_ensemble (stock_predict.models) -->
  <g transform="translate(40, 290)">
    <rect width="240" height="120" rx="4" fill="#ffffff" stroke="#000000" stroke-width="1.5"/>
    <rect x="-8" y="16" width="16" height="10" fill="#ffffff" stroke="#000000" stroke-width="1.2"/>
    <rect x="-8" y="36" width="16" height="10" fill="#ffffff" stroke="#000000" stroke-width="1.2"/>
    <text x="120" y="30" font-family="'Times New Roman', Times, serif" font-size="11" font-weight="700" fill="#000000" text-anchor="middle">&lt;&lt;component&gt;&gt;</text>
    <text x="120" y="48" font-family="'Times New Roman', Times, serif" font-size="11" font-weight="700" fill="#000000" text-anchor="middle">StackingMetaEnsemble</text>
    <text x="120" y="70" font-family="'Times New Roman', Times, serif" font-size="9" fill="#333333" text-anchor="middle">&bull; XGBoost (Taylor Objective)</text>
    <text x="120" y="85" font-family="'Times New Roman', Times, serif" font-size="9" fill="#333333" text-anchor="middle">&bull; LightGBM (GOSS &amp; EFB)</text>
    <text x="120" y="100" font-family="'Times New Roman', Times, serif" font-size="9" fill="#333333" text-anchor="middle">&bull; Random Forest &amp; AdaBoost</text>
  </g>

  <!-- COMPONENT 7: risk_execution_engine (stock_predict.core & backtest) -->
  <g transform="translate(200, 480)">
    <rect width="280" height="120" rx="4" fill="#ffffff" stroke="#000000" stroke-width="1.5"/>
    <rect x="-8" y="16" width="16" height="10" fill="#ffffff" stroke="#000000" stroke-width="1.2"/>
    <rect x="-8" y="36" width="16" height="10" fill="#ffffff" stroke="#000000" stroke-width="1.2"/>
    <text x="140" y="30" font-family="'Times New Roman', Times, serif" font-size="11" font-weight="700" fill="#000000" text-anchor="middle">&lt;&lt;component&gt;&gt;</text>
    <text x="140" y="48" font-family="'Times New Roman', Times, serif" font-size="11" font-weight="700" fill="#000000" text-anchor="middle">SelectiveRiskAndSizingEngine</text>
    <text x="140" y="70" font-family="'Times New Roman', Times, serif" font-size="9" fill="#333333" text-anchor="middle">&bull; Chow's Rejection Rule (&tau; &ge; 0.75)</text>
    <text x="140" y="85" font-family="'Times New Roman', Times, serif" font-size="9" fill="#333333" text-anchor="middle">&bull; Merton 2D Solver &amp; Altman Z Veto</text>
    <text x="140" y="100" font-family="'Times New Roman', Times, serif" font-size="9" fill="#333333" text-anchor="middle">&bull; Half-Kelly Position Sizer</text>
  </g>

  <!-- COMPONENT 8: hardware_telemetry (stock_predict.api) -->
  <g transform="translate(540, 480)">
    <rect width="280" height="120" rx="4" fill="#ffffff" stroke="#000000" stroke-width="1.5"/>
    <rect x="-8" y="16" width="16" height="10" fill="#ffffff" stroke="#000000" stroke-width="1.2"/>
    <rect x="-8" y="36" width="16" height="10" fill="#ffffff" stroke="#000000" stroke-width="1.2"/>
    <text x="140" y="30" font-family="'Times New Roman', Times, serif" font-size="11" font-weight="700" fill="#000000" text-anchor="middle">&lt;&lt;component&gt;&gt;</text>
    <text x="140" y="48" font-family="'Times New Roman', Times, serif" font-size="11" font-weight="700" fill="#000000" text-anchor="middle">SystemDiagnosticsTelemetry</text>
    <text x="140" y="70" font-family="'Times New Roman', Times, serif" font-size="9" fill="#333333" text-anchor="middle">&bull; PyTorch CUDA 12 Runtime Hook</text>
    <text x="140" y="85" font-family="'Times New Roman', Times, serif" font-size="9" fill="#333333" text-anchor="middle">&bull; RTX 3070 Ti VRAM Allocator</text>
    <text x="140" y="100" font-family="'Times New Roman', Times, serif" font-size="9" fill="#333333" text-anchor="middle">&bull; psutil Host RAM / Thread Gauge</text>
  </g>

  <!-- Interfaces & Dependencies (Dashed with arrow) -->
  <line x1="280" y1="145" x2="360" y2="145" stroke="#000000" stroke-width="1.5" stroke-dasharray="5,3" marker-end="url(#compArrow)"/>
  <text x="320" y="138" font-family="'Times New Roman', Times, serif" font-size="8" fill="#000000" text-anchor="middle">REST / WS</text>

  <line x1="610" y1="145" x2="680" y2="145" stroke="#000000" stroke-width="1.5" stroke-dasharray="5,3" marker-end="url(#compArrow)"/>
  <text x="645" y="138" font-family="'Times New Roman', Times, serif" font-size="8" fill="#000000" text-anchor="middle">fetch()</text>

  <line x1="800" y1="200" x2="800" y2="290" stroke="#000000" stroke-width="1.5" stroke-dasharray="5,3" marker-end="url(#compArrow)"/>
  <text x="810" y="245" font-family="'Times New Roman', Times, serif" font-size="8" fill="#000000">compute()</text>

  <line x1="680" y1="350" x2="610" y2="350" stroke="#000000" stroke-width="1.5" stroke-dasharray="5,3" marker-end="url(#compArrow)"/>
  <text x="645" y="342" font-family="'Times New Roman', Times, serif" font-size="8" fill="#000000" text-anchor="middle">tensors</text>

  <line x1="360" y1="350" x2="280" y2="350" stroke="#000000" stroke-width="1.5" stroke-dasharray="5,3" marker-end="url(#compArrow)"/>
  <text x="320" y="342" font-family="'Times New Roman', Times, serif" font-size="8" fill="#000000" text-anchor="middle">blend</text>

  <line x1="480" y1="410" x2="340" y2="480" stroke="#000000" stroke-width="1.5" stroke-dasharray="5,3" marker-end="url(#compArrow)"/>
  <text x="400" y="440" font-family="'Times New Roman', Times, serif" font-size="8" fill="#000000">posteriors</text>

  <line x1="485" y1="200" x2="680" y2="480" stroke="#000000" stroke-width="1.5" stroke-dasharray="5,3" marker-end="url(#compArrow)"/>
  <text x="560" y="440" font-family="'Times New Roman', Times, serif" font-size="8" fill="#000000">diagnostics</text>

  <!-- Bottom Substrate Label -->
  <rect x="40" y="630" width="880" height="40" rx="4" fill="#000000" stroke="#000000"/>
  <text x="480" y="655" font-family="'Times New Roman', Times, serif" font-size="10" font-weight="600" fill="#000000" text-anchor="middle">
    Execution Frameworks: PyTorch 2.x (CUDA 12.x), Scikit-Learn 1.4+, Statsmodels 0.14+, NumPy 2.x, FastAPI, Uvicorn
  </text>
</svg>'''

def get_uml_deployment_svg():
    return '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 960 700" width="100%" height="auto">
  <defs>
    
  </defs>

  <rect width="960" height="700" fill="#ffffff" stroke="#000000" stroke-width="1.2"/>

  <!-- Title -->
  <rect x="20" y="15" width="920" height="42" rx="6" fill="#000000" stroke="#000000"/>
  <text x="480" y="41" font-family="'Times New Roman', Times, serif" font-size="14" font-weight="700" fill="#ffffff" text-anchor="middle">
    UML DEPLOYMENT DIAGRAM: HARDWARE EXECUTION NODES &amp; DISTRIBUTED TOPOLOGY
  </text>

  <!-- NODE 1: Client Workstation -->
  <g transform="translate(40, 90)">
    <!-- 3D Box Top/Side -->
    <polygon points="10,0 230,0 220,15 0,15" fill="#f0f0f0" stroke="#000000"/>
    <polygon points="230,0 240,10 240,210 230,200" fill="#333333" stroke="#000000"/>
    <rect x="0" y="15" width="230" height="195" fill="#ffffff" stroke="#000000" stroke-width="1.5" rx="2"/>
    <text x="115" y="40" font-family="'Times New Roman', Times, serif" font-size="11" font-weight="700" fill="#000000" text-anchor="middle">&lt;&lt;device&gt;&gt;</text>
    <text x="115" y="56" font-family="'Times New Roman', Times, serif" font-size="11" font-weight="700" fill="#000000" text-anchor="middle">Trader Workstation</text>
    
    <!-- Nested Artifacts -->
    <rect x="20" y="75" width="190" height="55" rx="3" fill="#ffffff" stroke="#000000" stroke-width="1"/>
    <text x="115" y="96" font-family="'Times New Roman', Times, serif" font-size="9" font-weight="700" fill="#000000" text-anchor="middle">&lt;&lt;artifact&gt;&gt;</text>
    <text x="115" y="112" font-family="'Times New Roman', Times, serif" font-size="9" fill="#000000" text-anchor="middle">Modern Web Browser (Chrome/Edge)</text>

    <rect x="20" y="140" width="190" height="55" rx="3" fill="#ffffff" stroke="#000000" stroke-width="1"/>
    <text x="115" y="161" font-family="'Times New Roman', Times, serif" font-size="9" font-weight="700" fill="#000000" text-anchor="middle">&lt;&lt;artifact&gt;&gt;</text>
    <text x="115" y="177" font-family="'Times New Roman', Times, serif" font-size="9" fill="#000000" text-anchor="middle">TradingView Charts UI Engine</text>
  </g>

  <!-- NODE 2: Application & Ingestion Host -->
  <g transform="translate(360, 90)">
    <polygon points="10,0 270,0 260,15 0,15" fill="#f0f0f0" stroke="#000000"/>
    <polygon points="270,0 280,10 280,310 270,300" fill="#333333" stroke="#000000"/>
    <rect x="0" y="15" width="270" height="295" fill="#ffffff" stroke="#000000" stroke-width="1.5" rx="2"/>
    <text x="135" y="40" font-family="'Times New Roman', Times, serif" font-size="11" font-weight="700" fill="#000000" text-anchor="middle">&lt;&lt;device&gt;&gt;</text>
    <text x="135" y="56" font-family="'Times New Roman', Times, serif" font-size="11" font-weight="700" fill="#000000" text-anchor="middle">Local Host Server (Windows 11)</text>
    <text x="135" y="72" font-family="'Times New Roman', Times, serif" font-size="8" fill="#333333" text-anchor="middle">Intel/AMD 16-Thread CPU, 16 GB DDR4 RAM</text>

    <!-- Nested Execution Environments -->
    <rect x="20" y="85" width="230" height="95" rx="3" fill="#ffffff" stroke="#000000" stroke-width="1"/>
    <text x="135" y="105" font-family="'Times New Roman', Times, serif" font-size="9" font-weight="700" fill="#000000" text-anchor="middle">&lt;&lt;execution environment&gt;&gt;</text>
    <text x="135" y="120" font-family="'Times New Roman', Times, serif" font-size="9" font-weight="700" fill="#000000" text-anchor="middle">Python 3.10 Runtime</text>
    <text x="135" y="140" font-family="'Courier New', Courier, monospace" font-size="8" fill="#000000" text-anchor="middle">&bull; FastAPI Uvicorn Daemon (Port 8050)</text>
    <text x="135" y="155" font-family="'Courier New', Courier, monospace" font-size="8" fill="#000000" text-anchor="middle">&bull; Gradio Web App Server (Port 7860)</text>
    <text x="135" y="170" font-family="'Courier New', Courier, monospace" font-size="8" fill="#000000" text-anchor="middle">&bull; High-Speed TTL Cache (&lt;0.1ms)</text>

    <rect x="20" y="195" width="230" height="95" rx="3" fill="#ffffff" stroke="#000000" stroke-width="1"/>
    <text x="135" y="215" font-family="'Times New Roman', Times, serif" font-size="9" font-weight="700" fill="#000000" text-anchor="middle">&lt;&lt;file system&gt;&gt;</text>
    <text x="135" y="230" font-family="'Times New Roman', Times, serif" font-size="9" fill="#000000" text-anchor="middle">Disk Persistence Store</text>
    <text x="135" y="250" font-family="'Courier New', Courier, monospace" font-size="8" fill="#333333" text-anchor="middle">c:\projects\predict stock trends\</text>
    <text x="135" y="265" font-family="'Courier New', Courier, monospace" font-size="8" fill="#333333" text-anchor="middle">data_storage/*.csv | .sqlite</text>
  </g>

  <!-- NODE 3: GPU Compute Acceleration Node -->
  <g transform="translate(700, 90)">
    <polygon points="10,0 230,0 220,15 0,15" fill="#eeeeee" stroke="#000000"/>
    <polygon points="230,0 240,10 240,310 230,300" fill="#000000" stroke="#000000"/>
    <rect x="0" y="15" width="230" height="295" fill="#000000" stroke="#000000" stroke-width="1.5" rx="2"/>
    <text x="115" y="40" font-family="'Times New Roman', Times, serif" font-size="11" font-weight="700" fill="#000000" text-anchor="middle">&lt;&lt;accelerator&gt;&gt;</text>
    <text x="115" y="56" font-family="'Times New Roman', Times, serif" font-size="10" font-weight="700" fill="#ffffff" text-anchor="middle">NVIDIA GeForce RTX 3070 Ti</text>
    <text x="115" y="72" font-family="'Times New Roman', Times, serif" font-size="8" fill="#333333" text-anchor="middle">8,191.5 MB GDDR6 VRAM | Ampere GA104</text>

    <!-- Nested CUDA Artifacts -->
    <rect x="15" y="85" width="200" height="95" rx="3" fill="#000000" stroke="#000000" stroke-width="1"/>
    <text x="115" y="105" font-family="'Times New Roman', Times, serif" font-size="9" font-weight="700" fill="#000000" text-anchor="middle">&lt;&lt;runtime&gt;&gt;</text>
    <text x="115" y="120" font-family="'Times New Roman', Times, serif" font-size="9" font-weight="700" fill="#ffffff" text-anchor="middle">CUDA 12.x / cuDNN / TensorRT</text>
    <text x="115" y="140" font-family="'Courier New', Courier, monospace" font-size="8" fill="#f0f0f0" text-anchor="middle">&bull; PyTorchTCN Dilated Convolutions</text>
    <text x="115" y="155" font-family="'Courier New', Courier, monospace" font-size="8" fill="#f0f0f0" text-anchor="middle">&bull; PyTorchTFT Self-Attention VSN</text>
    <text x="115" y="170" font-family="'Courier New', Courier, monospace" font-size="8" fill="#f0f0f0" text-anchor="middle">&bull; BiLSTM with Bahdanau Attn</text>

    <rect x="15" y="195" width="200" height="95" rx="3" fill="#000000" stroke="#000000" stroke-width="1"/>
    <text x="115" y="215" font-family="'Times New Roman', Times, serif" font-size="9" font-weight="700" fill="#000000" text-anchor="middle">&lt;&lt;acceleration&gt;&gt;</text>
    <text x="115" y="230" font-family="'Times New Roman', Times, serif" font-size="9" font-weight="700" fill="#ffffff" text-anchor="middle">SIMD Vectorization Units</text>
    <text x="115" y="250" font-family="'Courier New', Courier, monospace" font-size="8" fill="#f0f0f0" text-anchor="middle">&bull; 1D FIR HMA 9 (35.2x speedup)</text>
    <text x="115" y="265" font-family="'Courier New', Courier, monospace" font-size="8" fill="#f0f0f0" text-anchor="middle">&bull; SuperTrend Traversal (28.8x)</text>
  </g>

  <!-- NODE 4: External Market Servers (Cloud) -->
  <g transform="translate(180, 460)">
    <polygon points="10,0 600,0 590,15 0,15" fill="#f0f0f0" stroke="#000000"/>
    <polygon points="600,0 610,10 610,180 600,170" fill="#000000" stroke="#000000"/>
    <rect x="0" y="15" width="600" height="165" fill="#ffffff" stroke="#000000" stroke-width="1.5" rx="2"/>
    <text x="300" y="38" font-family="'Times New Roman', Times, serif" font-size="11" font-weight="700" fill="#000000" text-anchor="middle">&lt;&lt;external cloud environments&gt;&gt;</text>
    <text x="300" y="54" font-family="'Times New Roman', Times, serif" font-size="11" font-weight="700" fill="#000000" text-anchor="middle">Financial Market Gateways &amp; WebSocket Endpoints</text>

    <!-- Sub-boxes for External Services -->
    <rect x="25" y="70" width="260" height="90" rx="3" fill="#ffffff" stroke="#000000" stroke-width="1"/>
    <text x="155" y="90" font-family="'Times New Roman', Times, serif" font-size="10" font-weight="700" fill="#000000" text-anchor="middle">National Stock Exchange (NSE India)</text>
    <text x="155" y="110" font-family="'Times New Roman', Times, serif" font-size="8" fill="#333333" text-anchor="middle">Yahoo Finance Historical &amp; Live Quotes</text>
    <text x="155" y="125" font-family="'Times New Roman', Times, serif" font-size="8" fill="#333333" text-anchor="middle">Trading Hours: 09:15 - 15:30 IST</text>
    <text x="155" y="140" font-family="'Times New Roman', Times, serif" font-size="8" fill="#333333" text-anchor="middle">Official Close Cross Freeze Integrity</text>

    <rect x="315" y="70" width="260" height="90" rx="3" fill="#ffffff" stroke="#000000" stroke-width="1"/>
    <text x="445" y="90" font-family="'Times New Roman', Times, serif" font-size="10" font-weight="700" fill="#000000" text-anchor="middle">Binance 24/7 WebSocket Cluster</text>
    <text x="445" y="110" font-family="'Times New Roman', Times, serif" font-size="8" fill="#333333" text-anchor="middle">wss://stream.binance.com:9443</text>
    <text x="445" y="125" font-family="'Times New Roman', Times, serif" font-size="8" fill="#333333" text-anchor="middle">Sub-second Trade Ticks &amp; L2 Order Depth</text>
    <text x="445" y="140" font-family="'Times New Roman', Times, serif" font-size="8" fill="#333333" text-anchor="middle">Uninterrupted 24/7/365 Streaming</text>
  </g>

  <!-- Network Connection Paths -->
  <!-- Client <-> Host -->
  <line x1="270" y1="180" x2="360" y2="180" stroke="#000000" stroke-width="2"/>
  <text x="315" y="172" font-family="'Times New Roman', Times, serif" font-size="8" font-weight="600" fill="#000000" text-anchor="middle">HTTP/JSON (8050)</text>
  <text x="315" y="195" font-family="'Times New Roman', Times, serif" font-size="8" font-weight="600" fill="#000000" text-anchor="middle">WS (8050/ws)</text>

  <!-- Host <-> GPU -->
  <line x1="630" y1="180" x2="700" y2="180" stroke="#000000" stroke-width="2"/>
  <text x="665" y="172" font-family="'Times New Roman', Times, serif" font-size="8" font-weight="600" fill="#000000" text-anchor="middle">PCIe 4.0 x16</text>
  <text x="665" y="195" font-family="'Times New Roman', Times, serif" font-size="8" font-weight="600" fill="#000000" text-anchor="middle">CUDA IPC / LibTorch</text>

  <!-- Host <-> Cloud External -->
  <line x1="495" y1="385" x2="495" y2="460" stroke="#000000" stroke-width="2"/>
  <text x="540" y="425" font-family="'Times New Roman', Times, serif" font-size="8" font-weight="600" fill="#000000">HTTPS / TLS 1.3 &amp; WSS</text>
</svg>'''

def get_uml_statechart_svg():
    return '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 960 700" width="100%" height="auto">
  <defs>
    
    <marker id="stateArrow" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto">
      <path d="M 0 1 L 10 5 L 0 9 z" fill="#000000"/>
    </marker>
  </defs>

  <rect width="960" height="700" fill="#ffffff" stroke="#000000" stroke-width="1.2"/>

  <!-- Title -->
  <rect x="20" y="15" width="920" height="42" rx="6" fill="#000000" stroke="#000000"/>
  <text x="480" y="41" font-family="'Times New Roman', Times, serif" font-size="14" font-weight="700" fill="#ffffff" text-anchor="middle">
    UML STATE-CHART DIAGRAM: PREDICTION &amp; EXECUTION SIGNAL LIFECYCLE
  </text>

  <!-- Initial State -->
  <circle cx="80" cy="150" r="12" fill="#000000" stroke="#000000"/>
  <line x1="92" y1="150" x2="140" y2="150" stroke="#000000" stroke-width="1.5" marker-end="url(#stateArrow)"/>
  <text x="115" y="142" font-family="'Times New Roman', Times, serif" font-size="8" fill="#333333" text-anchor="middle">start</text>

  <!-- STATE 1: IDLE -->
  <g transform="translate(140, 120)">
    <rect width="140" height="60" rx="8" fill="#ffffff" stroke="#000000" stroke-width="1.5"/>
    <text x="70" y="28" font-family="'Times New Roman', Times, serif" font-size="11" font-weight="700" fill="#000000" text-anchor="middle">1. IDLE</text>
    <text x="70" y="45" font-family="'Times New Roman', Times, serif" font-size="8" fill="#333333" text-anchor="middle">entry / await_request()</text>
  </g>

  <!-- Transition 1 -> 2 -->
  <line x1="280" y1="150" x2="350" y2="150" stroke="#000000" stroke-width="1.5" marker-end="url(#stateArrow)"/>
  <text x="315" y="142" font-family="'Times New Roman', Times, serif" font-size="8" fill="#000000" text-anchor="middle">req(ticker)</text>

  <!-- STATE 2: INGESTING_AND_CHECKING_LOCK -->
  <g transform="translate(350, 120)">
    <rect width="190" height="60" rx="8" fill="#ffffff" stroke="#000000" stroke-width="1.5"/>
    <text x="95" y="28" font-family="'Times New Roman', Times, serif" font-size="11" font-weight="700" fill="#000000" text-anchor="middle">2. INGESTING_SESSION</text>
    <text x="95" y="45" font-family="'Times New Roman', Times, serif" font-size="8" fill="#333333" text-anchor="middle">do / check_session_clock()</text>
  </g>

  <!-- Transition 2 -> 3 -->
  <line x1="540" y1="150" x2="610" y2="150" stroke="#000000" stroke-width="1.5" marker-end="url(#stateArrow)"/>
  <text x="575" y="142" font-family="'Times New Roman', Times, serif" font-size="8" fill="#000000" text-anchor="middle">data_clean</text>

  <!-- STATE 3: VECTORIZING_FEATURES -->
  <g transform="translate(610, 120)">
    <rect width="180" height="60" rx="8" fill="#ffffff" stroke="#000000" stroke-width="1.5"/>
    <text x="90" y="28" font-family="'Times New Roman', Times, serif" font-size="11" font-weight="700" fill="#000000" text-anchor="middle">3. VECTORIZING_SIGNALS</text>
    <text x="90" y="45" font-family="'Times New Roman', Times, serif" font-size="8" fill="#333333" text-anchor="middle">do / compute_26_features()</text>
  </g>

  <!-- Transition 3 -> 4 (Downwards) -->
  <line x1="700" y1="180" x2="700" y2="270" stroke="#000000" stroke-width="1.5" marker-end="url(#stateArrow)"/>
  <text x="710" y="225" font-family="'Times New Roman', Times, serif" font-size="8" fill="#000000">tensors_ready</text>

  <!-- STATE 4: TEMPORAL_CUDA_INFERENCE -->
  <g transform="translate(600, 270)">
    <rect width="200" height="65" rx="8" fill="#ffffff" stroke="#000000" stroke-width="1.5"/>
    <text x="100" y="28" font-family="'Times New Roman', Times, serif" font-size="11" font-weight="700" fill="#000000" text-anchor="middle">4. GPU_INFERENCE</text>
    <text x="100" y="44" font-family="'Times New Roman', Times, serif" font-size="8" fill="#333333" text-anchor="middle">do / ensemble_forward_cuda()</text>
    <text x="100" y="56" font-family="'Times New Roman', Times, serif" font-size="8" fill="#333333" text-anchor="middle">exit / posteriors_computed()</text>
  </g>

  <!-- Transition 4 -> 5 (Leftwards to Selective Evaluation) -->
  <line x1="600" y1="300" x2="480" y2="300" stroke="#000000" stroke-width="1.5" marker-end="url(#stateArrow)"/>
  <text x="540" y="292" font-family="'Times New Roman', Times, serif" font-size="8" fill="#000000" text-anchor="middle">eval_posteriors()</text>

  <!-- STATE 5: SELECTIVE_CLASSIFICATION_GATING -->
  <g transform="translate(260, 270)">
    <rect width="220" height="65" rx="8" fill="#ffffff" stroke="#000000" stroke-width="1.5"/>
    <text x="110" y="28" font-family="'Times New Roman', Times, serif" font-size="11" font-weight="700" fill="#000000" text-anchor="middle">5. CHOW_SELECTIVE_GATING</text>
    <text x="110" y="44" font-family="'Times New Roman', Times, serif" font-size="8" fill="#333333" text-anchor="middle">entry / compute_max_prob(g(x))</text>
    <text x="110" y="56" font-family="'Times New Roman', Times, serif" font-size="8" fill="#333333" text-anchor="middle">test / [g(x) &ge; 0.75]</text>
  </g>

  <!-- Branch A: [g(x) < 0.75] -> STATE 6A: ABSTAINED_CASH -->
  <line x1="260" y1="300" x2="160" y2="300" stroke="#000000" stroke-width="1.5" marker-end="url(#stateArrow)"/>
  <text x="210" y="290" font-family="'Times New Roman', Times, serif" font-size="8" font-weight="600" fill="#000000" text-anchor="middle">[g(x) &lt; 0.75]</text>

  <g transform="translate(30, 270)">
    <rect width="130" height="65" rx="8" fill="#ffffff" stroke="#000000" stroke-width="1.5"/>
    <text x="65" y="28" font-family="'Times New Roman', Times, serif" font-size="10" font-weight="700" fill="#000000" text-anchor="middle">6A. ABSTAINED</text>
    <text x="65" y="44" font-family="'Times New Roman', Times, serif" font-size="8" fill="#000000" text-anchor="middle">hold 100% cash</text>
    <text x="65" y="56" font-family="'Times New Roman', Times, serif" font-size="8" fill="#000000" text-anchor="middle">error bounded &le; 25%</text>
  </g>

  <!-- Branch B: [g(x) >= 0.75] -> STATE 6B: CREDIT_DISTRESS_CHECK -->
  <line x1="370" y1="335" x2="370" y2="430" stroke="#000000" stroke-width="1.5" marker-end="url(#stateArrow)"/>
  <text x="380" y="380" font-family="'Times New Roman', Times, serif" font-size="8" font-weight="600" fill="#000000">[g(x) &ge; 0.75]</text>

  <g transform="translate(260, 430)">
    <rect width="220" height="65" rx="8" fill="#ffffff" stroke="#000000" stroke-width="1.5"/>
    <text x="110" y="28" font-family="'Times New Roman', Times, serif" font-size="11" font-weight="700" fill="#000000" text-anchor="middle">6B. CREDIT_DISTRESS_CHECK</text>
    <text x="110" y="44" font-family="'Times New Roman', Times, serif" font-size="8" fill="#333333" text-anchor="middle">do / solve_merton_and_altman()</text>
    <text x="110" y="56" font-family="'Times New Roman', Times, serif" font-size="8" fill="#333333" text-anchor="middle">test / [Z &ge; 1.81 &amp;&amp; DD &ge; 1.5]</text>
  </g>

  <!-- Branch B1: Distress Veto -> STATE 7A: DISTRESS_VETO_HALT -->
  <line x1="260" y1="462" x2="160" y2="462" stroke="#000000" stroke-width="1.5" marker-end="url(#stateArrow)"/>
  <text x="210" y="452" font-family="'Times New Roman', Times, serif" font-size="8" font-weight="600" fill="#000000" text-anchor="middle">[Veto / Distress]</text>

  <g transform="translate(30, 430)">
    <rect width="130" height="65" rx="8" fill="#ffffff" stroke="#000000" stroke-width="1.5"/>
    <text x="65" y="28" font-family="'Times New Roman', Times, serif" font-size="10" font-weight="700" fill="#000000" text-anchor="middle">7A. VETO_HALT</text>
    <text x="65" y="44" font-family="'Times New Roman', Times, serif" font-size="8" fill="#000000" text-anchor="middle">Enron/SVB guard</text>
    <text x="65" y="56" font-family="'Times New Roman', Times, serif" font-size="8" fill="#000000" text-anchor="middle">cancel buy signal</text>
  </g>

  <!-- Branch B2: Distress Safe -> STATE 7B: HALF_KELLY_SIZING -->
  <line x1="480" y1="462" x2="570" y2="462" stroke="#000000" stroke-width="1.5" marker-end="url(#stateArrow)"/>
  <text x="525" y="452" font-family="'Times New Roman', Times, serif" font-size="8" font-weight="600" fill="#000000" text-anchor="middle">[Safe / Prime]</text>

  <g transform="translate(570, 430)">
    <rect width="210" height="65" rx="8" fill="#ffffff" stroke="#000000" stroke-width="1.5"/>
    <text x="105" y="28" font-family="'Times New Roman', Times, serif" font-size="11" font-weight="700" fill="#000000" text-anchor="middle">7B. HALF_KELLY_SIZING</text>
    <text x="105" y="44" font-family="'Times New Roman', Times, serif" font-size="8" fill="#333333" text-anchor="middle">do / compute_optimal_fraction()</text>
    <text x="105" y="56" font-family="'Times New Roman', Times, serif" font-size="8" fill="#333333" text-anchor="middle">exit / generate_action_plan()</text>
  </g>

  <!-- Transition 7B -> STATE 8: EXECUTING_ORDER -->
  <line x1="675" y1="495" x2="675" y2="560" stroke="#000000" stroke-width="1.5" marker-end="url(#stateArrow)"/>
  <text x="685" y="530" font-family="'Times New Roman', Times, serif" font-size="8" fill="#000000">plan_generated</text>

  <g transform="translate(570, 560)">
    <rect width="210" height="65" rx="8" fill="#ffffff" stroke="#000000" stroke-width="1.5"/>
    <text x="105" y="28" font-family="'Times New Roman', Times, serif" font-size="11" font-weight="700" fill="#000000" text-anchor="middle">8. ORDER_CONFIRMED</text>
    <text x="105" y="44" font-family="'Times New Roman', Times, serif" font-size="8" fill="#000000" text-anchor="middle">entry / publish_websocket()</text>
    <text x="105" y="56" font-family="'Times New Roman', Times, serif" font-size="8" fill="#000000" text-anchor="middle">win rate: 95.4% verified</text>
  </g>

  <!-- Transition to Final State -->
  <line x1="675" y1="625" x2="675" y2="660" stroke="#000000" stroke-width="1.5"/>
  <line x1="95" y1="335" x2="95" y2="660" stroke="#000000" stroke-width="1.5"/>
  <line x1="95" y1="495" x2="95" y2="660" stroke="#000000" stroke-width="1.5"/>
  <line x1="95" y1="660" x2="660" y2="660" stroke="#000000" stroke-width="1.5" marker-end="url(#stateArrow)"/>

  <!-- Final State (Bullseye) -->
  <g transform="translate(675, 660)">
    <circle cx="0" cy="0" r="14" fill="#ffffff" stroke="#000000" stroke-width="2"/>
    <circle cx="0" cy="0" r="8" fill="#000000" stroke="#000000"/>
  </g>
</svg>'''

def get_dfd_level_0_svg():
    return '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 960 520" width="100%" height="auto">
  <defs>
    
    <marker id="dfdArrow" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto">
      <path d="M 0 1 L 10 5 L 0 9 z" fill="#000000"/>
    </marker>
  </defs>

  <rect width="960" height="520" fill="#ffffff" stroke="#000000" stroke-width="1.2"/>

  <!-- Title -->
  <rect x="20" y="15" width="920" height="42" rx="6" fill="#000000" stroke="#000000"/>
  <text x="480" y="41" font-family="'Times New Roman', Times, serif" font-size="14" font-weight="700" fill="#ffffff" text-anchor="middle">
    DATA FLOW DIAGRAM (DFD) LEVEL 0: SYSTEM CONTEXT DIAGRAM
  </text>

  <!-- CENTRAL PROCESS: 0.0 StockTrend AI System -->
  <g transform="translate(360, 160)">
    <circle cx="120" cy="100" r="95" fill="#ffffff" stroke="#000000" stroke-width="2.5"/>
    <text x="120" y="80" font-family="'Times New Roman', Times, serif" font-size="12" font-weight="700" fill="#000000" text-anchor="middle">PROCESS 0.0</text>
    <text x="120" y="102" font-family="'Times New Roman', Times, serif" font-size="13" font-weight="700" fill="#000000" text-anchor="middle">AlphaTemporal</text>
    <text x="120" y="120" font-family="'Times New Roman', Times, serif" font-size="10" font-weight="600" fill="#000000" text-anchor="middle">StockTrend AI Platform</text>
    <text x="120" y="136" font-family="'Times New Roman', Times, serif" font-size="8" fill="#333333" text-anchor="middle">(CUDA Inference &amp; Risk Engine)</text>
  </g>

  <!-- EXTERNAL ENTITY 1: Trader / Portfolio Manager (Top Left) -->
  <g transform="translate(40, 100)">
    <rect width="180" height="70" fill="#ffffff" stroke="#000000" stroke-width="1.5" rx="3"/>
    <text x="90" y="32" font-family="'Times New Roman', Times, serif" font-size="11" font-weight="700" fill="#000000" text-anchor="middle">Quantitative Trader</text>
    <text x="90" y="50" font-family="'Times New Roman', Times, serif" font-size="8" fill="#333333" text-anchor="middle">&lt;&lt;External Entity&gt;&gt;</text>
  </g>

  <!-- EXTERNAL ENTITY 2: Risk Officer / Auditor (Bottom Left) -->
  <g transform="translate(40, 310)">
    <rect width="180" height="70" fill="#ffffff" stroke="#000000" stroke-width="1.5" rx="3"/>
    <text x="90" y="32" font-family="'Times New Roman', Times, serif" font-size="11" font-weight="700" fill="#000000" text-anchor="middle">Risk Officer / Auditor</text>
    <text x="90" y="50" font-family="'Times New Roman', Times, serif" font-size="8" fill="#333333" text-anchor="middle">&lt;&lt;External Entity&gt;&gt;</text>
  </g>

  <!-- EXTERNAL ENTITY 3: National Stock Exchange (Top Right) -->
  <g transform="translate(740, 100)">
    <rect width="180" height="70" fill="#ffffff" stroke="#000000" stroke-width="1.5" rx="3"/>
    <text x="90" y="32" font-family="'Times New Roman', Times, serif" font-size="11" font-weight="700" fill="#000000" text-anchor="middle">NSE Market Data Gateway</text>
    <text x="90" y="50" font-family="'Times New Roman', Times, serif" font-size="8" fill="#333333" text-anchor="middle">&lt;&lt;External Data Source&gt;&gt;</text>
  </g>

  <!-- EXTERNAL ENTITY 4: Binance WebSocket Gateway (Bottom Right) -->
  <g transform="translate(740, 310)">
    <rect width="180" height="70" fill="#ffffff" stroke="#000000" stroke-width="1.5" rx="3"/>
    <text x="90" y="32" font-family="'Times New Roman', Times, serif" font-size="11" font-weight="700" fill="#000000" text-anchor="middle">Binance Crypto Gateway</text>
    <text x="90" y="50" font-family="'Times New Roman', Times, serif" font-size="8" fill="#333333" text-anchor="middle">&lt;&lt;External Data Source&gt;&gt;</text>
  </g>

  <!-- Data Flows: Trader <-> System -->
  <line x1="220" y1="125" x2="375" y2="200" stroke="#000000" stroke-width="1.5" marker-end="url(#dfdArrow)"/>
  <text x="280" y="150" font-family="'Times New Roman', Times, serif" font-size="8" fill="#000000">Ticker &amp; Horizon Queries</text>

  <line x1="375" y1="230" x2="220" y2="155" stroke="#000000" stroke-width="1.5" marker-end="url(#dfdArrow)"/>
  <text x="280" y="205" font-family="'Times New Roman', Times, serif" font-size="8" fill="#000000">Trade Action Plan &amp; Half-Kelly</text>

  <!-- Data Flows: Risk Officer <-> System -->
  <line x1="220" y1="335" x2="385" y2="295" stroke="#000000" stroke-width="1.5" marker-end="url(#dfdArrow)"/>
  <text x="280" y="310" font-family="'Times New Roman', Times, serif" font-size="8" fill="#000000">Audit &amp; Stress Parameters</text>

  <line x1="385" y1="315" x2="220" y2="365" stroke="#000000" stroke-width="1.5" marker-end="url(#dfdArrow)"/>
  <text x="280" y="355" font-family="'Times New Roman', Times, serif" font-size="8" fill="#000000">Merton DD &amp; Altman Z Veto Logs</text>

  <!-- Data Flows: NSE -> System -->
  <line x1="740" y1="140" x2="575" y2="210" stroke="#000000" stroke-width="1.5" marker-end="url(#dfdArrow)"/>
  <text x="680" y="165" font-family="'Times New Roman', Times, serif" font-size="8" fill="#000000" text-anchor="middle">09:15-15:30 IST OHLCV Feeds</text>

  <!-- Data Flows: Binance -> System -->
  <line x1="740" y1="340" x2="575" y2="290" stroke="#000000" stroke-width="1.5" marker-end="url(#dfdArrow)"/>
  <text x="680" y="325" font-family="'Times New Roman', Times, serif" font-size="8" fill="#000000" text-anchor="middle">24/7 Sub-sec WebSocket Ticks</text>
</svg>'''

def get_dfd_level_1_svg():
    return '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 960 720" width="100%" height="auto">
  <defs>
    
    <marker id="dfd1Arrow" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto">
      <path d="M 0 1 L 10 5 L 0 9 z" fill="#000000"/>
    </marker>
  </defs>

  <rect width="960" height="720" fill="#ffffff" stroke="#000000" stroke-width="1.2"/>

  <!-- Title -->
  <rect x="20" y="15" width="920" height="42" rx="6" fill="#000000" stroke="#000000"/>
  <text x="480" y="41" font-family="'Times New Roman', Times, serif" font-size="14" font-weight="700" fill="#ffffff" text-anchor="middle">
    DATA FLOW DIAGRAM (DFD) LEVEL 1: SUBSYSTEM DECOMPOSITION &amp; DATA STORES
  </text>

  <!-- PROCESS 1.0: Ingestion & Session Lock -->
  <g transform="translate(60, 90)">
    <circle cx="50" cy="50" r="45" fill="#ffffff" stroke="#000000" stroke-width="2"/>
    <text x="50" y="42" font-family="'Times New Roman', Times, serif" font-size="10" font-weight="700" fill="#000000" text-anchor="middle">1.0</text>
    <text x="50" y="58" font-family="'Times New Roman', Times, serif" font-size="9" font-weight="600" fill="#000000" text-anchor="middle">Ingestion &amp;</text>
    <text x="50" y="70" font-family="'Times New Roman', Times, serif" font-size="8" fill="#333333" text-anchor="middle">Session Lock</text>
  </g>

  <!-- DATA STORE D1: Raw Price Store -->
  <g transform="translate(230, 90)">
    <line x1="0" y1="30" x2="140" y2="30" stroke="#000000" stroke-width="2"/>
    <line x1="0" y1="70" x2="140" y2="70" stroke="#000000" stroke-width="2"/>
    <rect x="0" y="30" width="140" height="40" fill="#ffffff"/>
    <text x="15" y="54" font-family="'Courier New', Courier, monospace" font-size="9" font-weight="700" fill="#000000">D1</text>
    <text x="75" y="54" font-family="'Times New Roman', Times, serif" font-size="9" fill="#000000" text-anchor="middle">Raw Candles (1D)</text>
  </g>

  <!-- PROCESS 2.0: Signal Vectorization & Differencing -->
  <g transform="translate(440, 90)">
    <circle cx="50" cy="50" r="45" fill="#ffffff" stroke="#000000" stroke-width="2"/>
    <text x="50" y="42" font-family="'Times New Roman', Times, serif" font-size="10" font-weight="700" fill="#000000" text-anchor="middle">2.0</text>
    <text x="50" y="58" font-family="'Times New Roman', Times, serif" font-size="9" font-weight="600" fill="#000000" text-anchor="middle">Feature Matrix</text>
    <text x="50" y="70" font-family="'Times New Roman', Times, serif" font-size="8" fill="#333333" text-anchor="middle">&amp; FracDiff d*</text>
  </g>

  <!-- DATA STORE D2: Feature Matrix Store -->
  <g transform="translate(610, 90)">
    <line x1="0" y1="30" x2="150" y2="30" stroke="#000000" stroke-width="2"/>
    <line x1="0" y1="70" x2="150" y2="70" stroke="#000000" stroke-width="2"/>
    <rect x="0" y="30" width="150" height="40" fill="#ffffff"/>
    <text x="15" y="54" font-family="'Courier New', Courier, monospace" font-size="9" font-weight="700" fill="#000000">D2</text>
    <text x="80" y="54" font-family="'Times New Roman', Times, serif" font-size="9" fill="#000000" text-anchor="middle">26 Indicators Matrix</text>
  </g>

  <!-- PROCESS 3.0: Deep Learning & ML Inference -->
  <g transform="translate(820, 90)">
    <circle cx="50" cy="50" r="45" fill="#ffffff" stroke="#000000" stroke-width="2"/>
    <text x="50" y="42" font-family="'Times New Roman', Times, serif" font-size="10" font-weight="700" fill="#000000" text-anchor="middle">3.0</text>
    <text x="50" y="58" font-family="'Times New Roman', Times, serif" font-size="9" font-weight="600" fill="#000000" text-anchor="middle">AI Ensemble</text>
    <text x="50" y="70" font-family="'Times New Roman', Times, serif" font-size="8" fill="#333333" text-anchor="middle">(TFT / TCN / Meta)</text>
  </g>

  <!-- DATA STORE D3: Inference Posteriors Store -->
  <g transform="translate(730, 270)">
    <line x1="0" y1="30" x2="150" y2="30" stroke="#000000" stroke-width="2"/>
    <line x1="0" y1="70" x2="150" y2="70" stroke="#000000" stroke-width="2"/>
    <rect x="0" y="30" width="150" height="40" fill="#ffffff"/>
    <text x="15" y="54" font-family="'Courier New', Courier, monospace" font-size="9" font-weight="700" fill="#000000">D3</text>
    <text x="80" y="54" font-family="'Times New Roman', Times, serif" font-size="9" fill="#000000" text-anchor="middle">Posteriors [P(Up)]</text>
  </g>

  <!-- PROCESS 4.0: Selective Classification (Chow Rule) -->
  <g transform="translate(440, 260)">
    <circle cx="50" cy="50" r="45" fill="#ffffff" stroke="#000000" stroke-width="2"/>
    <text x="50" y="42" font-family="'Times New Roman', Times, serif" font-size="10" font-weight="700" fill="#000000" text-anchor="middle">4.0</text>
    <text x="50" y="58" font-family="'Times New Roman', Times, serif" font-size="9" font-weight="600" fill="#000000" text-anchor="middle">Chow Gating</text>
    <text x="50" y="70" font-family="'Times New Roman', Times, serif" font-size="8" fill="#333333" text-anchor="middle">(&tau; &ge; 0.75 Rule)</text>
  </g>

  <!-- DATA STORE D4: Confirmed High-Conviction Decisions -->
  <g transform="translate(230, 270)">
    <line x1="0" y1="30" x2="140" y2="30" stroke="#000000" stroke-width="2"/>
    <line x1="0" y1="70" x2="140" y2="70" stroke="#000000" stroke-width="2"/>
    <rect x="0" y="30" width="140" height="40" fill="#ffffff"/>
    <text x="15" y="54" font-family="'Courier New', Courier, monospace" font-size="9" font-weight="700" fill="#000000">D4</text>
    <text x="75" y="54" font-family="'Times New Roman', Times, serif" font-size="9" fill="#000000" text-anchor="middle">Selected Trades</text>
  </g>

  <!-- PROCESS 5.0: Credit Distress & Veto Engine -->
  <g transform="translate(60, 260)">
    <circle cx="50" cy="50" r="45" fill="#ffffff" stroke="#000000" stroke-width="2"/>
    <text x="50" y="42" font-family="'Times New Roman', Times, serif" font-size="10" font-weight="700" fill="#000000" text-anchor="middle">5.0</text>
    <text x="50" y="58" font-family="'Times New Roman', Times, serif" font-size="9" font-weight="600" fill="#000000" text-anchor="middle">Credit Risk</text>
    <text x="50" y="70" font-family="'Times New Roman', Times, serif" font-size="8" fill="#333333" text-anchor="middle">(Merton + Altman)</text>
  </g>

  <!-- PROCESS 6.0: Portfolio Sizing & Execution Plan -->
  <g transform="translate(250, 470)">
    <circle cx="50" cy="50" r="45" fill="#ffffff" stroke="#000000" stroke-width="2"/>
    <text x="50" y="42" font-family="'Times New Roman', Times, serif" font-size="10" font-weight="700" fill="#000000" text-anchor="middle">6.0</text>
    <text x="50" y="58" font-family="'Times New Roman', Times, serif" font-size="9" font-weight="600" fill="#000000" text-anchor="middle">Half-Kelly</text>
    <text x="50" y="70" font-family="'Times New Roman', Times, serif" font-size="8" fill="#333333" text-anchor="middle">Allocation Plan</text>
  </g>

  <!-- DATA STORE D5: Action Plans & Backtest Logs -->
  <g transform="translate(540, 480)">
    <line x1="0" y1="30" x2="170" y2="30" stroke="#000000" stroke-width="2"/>
    <line x1="0" y1="70" x2="170" y2="70" stroke="#000000" stroke-width="2"/>
    <rect x="0" y="30" width="170" height="40" fill="#ffffff"/>
    <text x="15" y="54" font-family="'Courier New', Courier, monospace" font-size="9" font-weight="700" fill="#000000">D5</text>
    <text x="90" y="54" font-family="'Times New Roman', Times, serif" font-size="9" fill="#000000" text-anchor="middle">Trading Action Plans</text>
  </g>

  <!-- DFD Connections -->
  <line x1="150" y1="140" x2="230" y2="140" stroke="#000000" stroke-width="1.5" marker-end="url(#dfd1Arrow)"/>
  <line x1="370" y1="140" x2="440" y2="140" stroke="#000000" stroke-width="1.5" marker-end="url(#dfd1Arrow)"/>
  <line x1="530" y1="140" x2="610" y2="140" stroke="#000000" stroke-width="1.5" marker-end="url(#dfd1Arrow)"/>
  <line x1="760" y1="140" x2="820" y2="140" stroke="#000000" stroke-width="1.5" marker-end="url(#dfd1Arrow)"/>

  <!-- 3.0 to D3 -->
  <line x1="870" y1="180" x2="870" y2="320" stroke="#000000" stroke-width="1.5"/>
  <line x1="870" y1="320" x2="880" y2="320" stroke="#000000" stroke-width="1.5" marker-end="url(#dfd1Arrow)"/>

  <!-- D3 to 4.0 -->
  <line x1="730" y1="310" x2="530" y2="310" stroke="#000000" stroke-width="1.5" marker-end="url(#dfd1Arrow)"/>

  <!-- 4.0 to D4 -->
  <line x1="440" y1="310" x2="370" y2="310" stroke="#000000" stroke-width="1.5" marker-end="url(#dfd1Arrow)"/>

  <!-- D4 to 5.0 -->
  <line x1="230" y1="310" x2="150" y2="310" stroke="#000000" stroke-width="1.5" marker-end="url(#dfd1Arrow)"/>

  <!-- 5.0 to 6.0 -->
  <line x1="110" y1="350" x2="110" y2="520" stroke="#000000" stroke-width="1.5"/>
  <line x1="110" y1="520" x2="250" y2="520" stroke="#000000" stroke-width="1.5" marker-end="url(#dfd1Arrow)"/>

  <!-- 6.0 to D5 -->
  <line x1="340" y1="520" x2="540" y2="520" stroke="#000000" stroke-width="1.5" marker-end="url(#dfd1Arrow)"/>
</svg>'''

def get_dfd_level_2_svg():
    return '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 960 680" width="100%" height="auto">
  <defs>
    
    <marker id="dfd2Arrow" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto">
      <path d="M 0 1 L 10 5 L 0 9 z" fill="#000000"/>
    </marker>
  </defs>

  <rect width="960" height="680" fill="#ffffff" stroke="#000000" stroke-width="1.2"/>

  <!-- Title -->
  <rect x="20" y="15" width="920" height="42" rx="6" fill="#000000" stroke="#000000"/>
  <text x="480" y="41" font-family="'Times New Roman', Times, serif" font-size="14" font-weight="700" fill="#ffffff" text-anchor="middle">
    DATA FLOW DIAGRAM (DFD) LEVEL 2: DEEP DIVE PROCESS 3.0 (AI INFERENCE) &amp; 4.0 (CHOW GATING)
  </text>

  <!-- Input Store: D2 Feature Matrix -->
  <g transform="translate(40, 100)">
    <line x1="0" y1="20" x2="130" y2="20" stroke="#000000" stroke-width="2"/>
    <line x1="0" y1="60" x2="130" y2="60" stroke="#000000" stroke-width="2"/>
    <rect x="0" y="20" width="130" height="40" fill="#ffffff"/>
    <text x="15" y="44" font-family="'Courier New', Courier, monospace" font-size="9" font-weight="700" fill="#000000">D2</text>
    <text x="70" y="44" font-family="'Times New Roman', Times, serif" font-size="8" fill="#000000" text-anchor="middle">26 Indicators</text>
  </g>

  <!-- SUB-PROCESS 3.1: Sequence Formatter -->
  <g transform="translate(230, 90)">
    <circle cx="45" cy="45" r="40" fill="#ffffff" stroke="#000000" stroke-width="2"/>
    <text x="45" y="38" font-family="'Times New Roman', Times, serif" font-size="9" font-weight="700" fill="#000000" text-anchor="middle">3.1</text>
    <text x="45" y="52" font-family="'Times New Roman', Times, serif" font-size="8" font-weight="600" fill="#000000" text-anchor="middle">Sequence</text>
    <text x="45" y="64" font-family="'Times New Roman', Times, serif" font-size="7" fill="#333333" text-anchor="middle">Sliding Window</text>
  </g>

  <!-- SUB-PROCESS 3.2: TCN Dilated Convolutions -->
  <g transform="translate(400, 90)">
    <circle cx="45" cy="45" r="40" fill="#ffffff" stroke="#000000" stroke-width="2"/>
    <text x="45" y="38" font-family="'Times New Roman', Times, serif" font-size="9" font-weight="700" fill="#000000" text-anchor="middle">3.2</text>
    <text x="45" y="52" font-family="'Times New Roman', Times, serif" font-size="8" font-weight="600" fill="#000000" text-anchor="middle">TCN Dilated</text>
    <text x="45" y="64" font-family="'Times New Roman', Times, serif" font-size="7" fill="#333333" text-anchor="middle">RF=61 Convolutions</text>
  </g>

  <!-- SUB-PROCESS 3.3: TFT Variable Selection & Attention -->
  <g transform="translate(570, 90)">
    <circle cx="45" cy="45" r="40" fill="#ffffff" stroke="#000000" stroke-width="2"/>
    <text x="45" y="38" font-family="'Times New Roman', Times, serif" font-size="9" font-weight="700" fill="#000000" text-anchor="middle">3.3</text>
    <text x="45" y="52" font-family="'Times New Roman', Times, serif" font-size="8" font-weight="600" fill="#000000" text-anchor="middle">TFT Self-Attn</text>
    <text x="45" y="64" font-family="'Times New Roman', Times, serif" font-size="7" fill="#333333" text-anchor="middle">VSN + GRN Gating</text>
  </g>

  <!-- SUB-PROCESS 3.4: Stacking Meta-Learner Blend -->
  <g transform="translate(740, 90)">
    <circle cx="45" cy="45" r="40" fill="#ffffff" stroke="#000000" stroke-width="2"/>
    <text x="45" y="38" font-family="'Times New Roman', Times, serif" font-size="9" font-weight="700" fill="#000000" text-anchor="middle">3.4</text>
    <text x="45" y="52" font-family="'Times New Roman', Times, serif" font-size="8" font-weight="600" fill="#000000" text-anchor="middle">Meta-Learner</text>
    <text x="45" y="64" font-family="'Times New Roman', Times, serif" font-size="7" fill="#333333" text-anchor="middle">OOF Probability Blend</text>
  </g>

  <!-- PROCESS 4 DECOMPOSITION (Below) -->
  <!-- SUB-PROCESS 4.1: Calibrated Posterior Extractor -->
  <g transform="translate(740, 310)">
    <circle cx="45" cy="45" r="40" fill="#ffffff" stroke="#000000" stroke-width="2"/>
    <text x="45" y="38" font-family="'Times New Roman', Times, serif" font-size="9" font-weight="700" fill="#000000" text-anchor="middle">4.1</text>
    <text x="45" y="52" font-family="'Times New Roman', Times, serif" font-size="8" font-weight="600" fill="#000000" text-anchor="middle">Extract g(x)</text>
    <text x="45" y="64" font-family="'Times New Roman', Times, serif" font-size="7" fill="#333333" text-anchor="middle">max P(Y=k|x)</text>
  </g>

  <!-- SUB-PROCESS 4.2: Chow Threshold Evaluator -->
  <g transform="translate(510, 310)">
    <circle cx="45" cy="45" r="40" fill="#ffffff" stroke="#000000" stroke-width="2"/>
    <text x="45" y="38" font-family="'Times New Roman', Times, serif" font-size="9" font-weight="700" fill="#000000" text-anchor="middle">4.2</text>
    <text x="45" y="52" font-family="'Times New Roman', Times, serif" font-size="8" font-weight="600" fill="#000000" text-anchor="middle">Evaluate &tau;</text>
    <text x="45" y="64" font-family="'Times New Roman', Times, serif" font-size="7" fill="#333333" text-anchor="middle">&tau; = 0.75 Rule</text>
  </g>

  <!-- SUB-PROCESS 4.3: Error Bounding & Signal Route -->
  <g transform="translate(280, 310)">
    <circle cx="45" cy="45" r="40" fill="#ffffff" stroke="#000000" stroke-width="2"/>
    <text x="45" y="38" font-family="'Times New Roman', Times, serif" font-size="9" font-weight="700" fill="#000000" text-anchor="middle">4.3</text>
    <text x="45" y="52" font-family="'Times New Roman', Times, serif" font-size="8" font-weight="600" fill="#000000" text-anchor="middle">Bound Error</text>
    <text x="45" y="64" font-family="'Times New Roman', Times, serif" font-size="7" fill="#333333" text-anchor="middle">&epsilon;(x) &le; 1 - &tau;</text>
  </g>

  <!-- Outputs: Abstain vs Execution Route -->
  <g transform="translate(60, 290)">
    <rect width="140" height="40" rx="4" fill="#ffffff" stroke="#000000" stroke-width="1.5"/>
    <text x="70" y="24" font-family="'Times New Roman', Times, serif" font-size="9" font-weight="700" fill="#000000" text-anchor="middle">ABSTAIN (Hold Cash)</text>
  </g>

  <g transform="translate(60, 360)">
    <rect width="140" height="40" rx="4" fill="#ffffff" stroke="#000000" stroke-width="1.5"/>
    <text x="70" y="24" font-family="'Times New Roman', Times, serif" font-size="9" font-weight="700" fill="#000000" text-anchor="middle">HIGH-CONVICTION TRADE</text>
  </g>

  <!-- Flows Level 2 -->
  <line x1="170" y1="135" x2="230" y2="135" stroke="#000000" stroke-width="1.5" marker-end="url(#dfd2Arrow)"/>
  <line x1="310" y1="135" x2="400" y2="135" stroke="#000000" stroke-width="1.5" marker-end="url(#dfd2Arrow)"/>
  <line x1="480" y1="135" x2="570" y2="135" stroke="#000000" stroke-width="1.5" marker-end="url(#dfd2Arrow)"/>
  <line x1="650" y1="135" x2="740" y2="135" stroke="#000000" stroke-width="1.5" marker-end="url(#dfd2Arrow)"/>

  <!-- 3.4 to 4.1 -->
  <line x1="785" y1="170" x2="785" y2="310" stroke="#000000" stroke-width="1.5" marker-end="url(#dfd2Arrow)"/>

  <!-- 4.1 to 4.2 -->
  <line x1="740" y1="350" x2="590" y2="350" stroke="#000000" stroke-width="1.5" marker-end="url(#dfd2Arrow)"/>

  <!-- 4.2 to 4.3 -->
  <line x1="510" y1="350" x2="360" y2="350" stroke="#000000" stroke-width="1.5" marker-end="url(#dfd2Arrow)"/>

  <!-- 4.3 to Abstain -->
  <line x1="280" y1="330" x2="200" y2="310" stroke="#000000" stroke-width="1.5" marker-end="url(#dfd2Arrow)"/>

  <!-- 4.3 to High Conviction -->
  <line x1="280" y1="365" x2="200" y2="380" stroke="#000000" stroke-width="1.5" marker-end="url(#dfd2Arrow)"/>
</svg>'''
