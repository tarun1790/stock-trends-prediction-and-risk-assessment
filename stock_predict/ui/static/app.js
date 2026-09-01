/**
 * Stock Market Trend Prediction Platform - Frontend Application
 * Interacts with FastAPI backend to render real-time charts, model benchmarks,
 * live trend predictions, and quantitative backtesting.
 */

document.addEventListener("DOMContentLoaded", () => {
  // Initialize Lucide Icons
  lucide.createIcons();

  // State
  let currentIndicatorsData = null;
  let priceChartInstance = null;
  let benchmarkChartInstance = null;
  let equityChartInstance = null;

  // DOM Elements
  const tabBtns = document.querySelectorAll(".tab-btn");
  const tabContents = document.querySelectorAll(".tab-content");
  const sectorSelect = document.getElementById("sector-select");
  const customTickerInput = document.getElementById("custom-ticker-input");
  const btnCustomTicker = document.getElementById("btn-custom-ticker");
  const btnRefreshData = document.getElementById("btn-refresh-data");
  const overlaySelect = document.getElementById("indicator-overlay-select");

  const btnRunBenchmark = document.getElementById("btn-run-benchmark");
  const btnRunPrediction = document.getElementById("btn-run-prediction");
  const btnRunBacktest = document.getElementById("btn-run-backtest");

  // -----------------------------------------------------------------------
  // 1. Tab Switching
  // -----------------------------------------------------------------------
  tabBtns.forEach((btn) => {
    btn.addEventListener("click", () => {
      tabBtns.forEach((b) => {
        b.classList.remove("active-tab", "text-white");
        b.classList.add("text-slate-400");
      });
      btn.classList.add("active-tab", "text-white");
      btn.classList.remove("text-slate-400");

      const targetId = btn.getAttribute("data-tab");
      tabContents.forEach((c) => {
        if (c.id === targetId) {
          c.classList.remove("hidden");
        } else {
          c.classList.add("hidden");
        }
      });
      lucide.createIcons();
    });
  });

  // -----------------------------------------------------------------------
  // 2. Fetch System Status (GPU & CUDA)
  // -----------------------------------------------------------------------
  async function checkSystemStatus() {
    try {
      const res = await fetch("/api/status");
      const data = await res.json();
      const gpuBadge = document.getElementById("gpu-badge");
      const gpuText = document.getElementById("gpu-status-text");

      if (data.cuda_available) {
        gpuBadge.className = "flex items-center space-x-2 bg-emerald-950/80 border border-emerald-800/80 text-emerald-400 text-xs px-3 py-1.5 rounded-full font-medium shadow-sm";
        gpuText.textContent = data.gpu_name ? `GPU: ${data.gpu_name}` : "CUDA GPU Active";
      } else {
        gpuBadge.className = "flex items-center space-x-2 bg-amber-950/80 border border-amber-800/80 text-amber-400 text-xs px-3 py-1.5 rounded-full font-medium shadow-sm";
        gpuText.textContent = "CPU Execution";
      }
    } catch (e) {
      console.warn("Status check error:", e);
    }
  }

  // -----------------------------------------------------------------------
  // 3. Data Ingestion & Technical Indicators
  // -----------------------------------------------------------------------
  async function loadMarketAndIndicators() {
    const isTicker = ["AAPL", "NVDA", "MSFT", "TSLA", "SPY", "BTC-USD", "CL=F"].includes(
      sectorSelect.value
    ) || customTickerInput.value.trim() !== "";

    const payload = {};
    if (customTickerInput.value.trim() !== "") {
      payload.source = "ticker";
      payload.ticker = customTickerInput.value.trim().toUpperCase();
    } else if (isTicker) {
      payload.source = "ticker";
      payload.ticker = sectorSelect.value;
    } else {
      payload.source = "sample";
      payload.sector_key = sectorSelect.value;
    }

    const assetName = payload.ticker || sectorSelect.options[sectorSelect.selectedIndex].text;
    document.getElementById("asset-subtitle").textContent = `${assetName} Daily Historical Series`;
    document.getElementById("predict-ticker-badge").textContent = assetName;

    try {
      const res = await fetch("/api/indicators/compute", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });

      const data = await res.json();
      currentIndicatorsData = data.records;

      renderPriceChart();
      renderIndicatorCards();
      renderIndicatorTable();
      renderBinaryTable();
    } catch (err) {
      console.error("Failed to load indicators:", err);
    }
  }

  // Render Price & Indicator Overlay Chart
  function renderPriceChart() {
    if (!currentIndicatorsData || currentIndicatorsData.length === 0) return;

    const ctx = document.getElementById("price-chart").getContext("2d");
    const labels = currentIndicatorsData.map((d) => d.date);
    const closePrices = currentIndicatorsData.map((d) => d.close);
    const selectedOverlay = overlaySelect.value.toLowerCase();
    const overlayValues = currentIndicatorsData.map((d) => d[selectedOverlay]);

    if (priceChartInstance) {
      priceChartInstance.destroy();
    }

    const datasets = [
      {
        label: "Close Price",
        data: closePrices,
        borderColor: "#6366f1",
        backgroundColor: "rgba(99, 102, 241, 0.1)",
        borderWidth: 2,
        fill: true,
        tension: 0.1,
        yAxisID: "y",
      },
      {
        label: `${overlaySelect.value} Indicator`,
        data: overlayValues,
        borderColor: "#10b981",
        borderWidth: 1.8,
        borderDash: [4, 4],
        pointRadius: 0,
        fill: false,
        tension: 0.1,
        yAxisID: ["rsi", "stck", "stcd", "lwr", "ado", "cci", "mom"].includes(selectedOverlay)
          ? "y1"
          : "y",
      },
    ];

    priceChartInstance = new Chart(ctx, {
      type: "line",
      data: { labels, datasets },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        interaction: { mode: "index", intersect: false },
        plugins: {
          legend: { labels: { color: "#94a3b8", font: { size: 11 } } },
          tooltip: {
            backgroundColor: "#0f172a",
            borderColor: "#334155",
            borderWidth: 1,
            titleColor: "#f8fafc",
            bodyColor: "#cbd5e1",
          },
        },
        scales: {
          x: {
            grid: { color: "#1e293b" },
            ticks: { color: "#64748b", maxTicksLimit: 12 },
          },
          y: {
            position: "left",
            grid: { color: "#1e293b" },
            ticks: { color: "#64748b" },
          },
          y1: {
            position: "right",
            display: ["rsi", "stck", "stcd", "lwr", "ado", "cci", "mom"].includes(selectedOverlay),
            grid: { drawOnChartArea: false },
            ticks: { color: "#10b981" },
          },
        },
      },
    });
  }

  // Render Indicator Value Cards
  function renderIndicatorCards() {
    if (!currentIndicatorsData || currentIndicatorsData.length === 0) return;
    const latest = currentIndicatorsData[currentIndicatorsData.length - 1];
    const grid = document.getElementById("indicator-cards-grid");

    const indicators = [
      { name: "SMA (10)", val: latest.sma, bin: latest.binary_signals?.SMA },
      { name: "WMA (10)", val: latest.wma, bin: latest.binary_signals?.WMA },
      { name: "Momentum", val: latest.mom, bin: latest.binary_signals?.MOM },
      { name: "Stoch %K", val: latest.stck, bin: latest.binary_signals?.STCK },
      { name: "Stoch %D", val: latest.stcd, bin: latest.binary_signals?.STCD },
      { name: "RSI (10)", val: latest.rsi, bin: latest.binary_signals?.RSI },
      { name: "MACD Sig", val: latest.sig, bin: latest.binary_signals?.SIG },
      { name: "Larry's %R", val: latest.lwr, bin: latest.binary_signals?.LWR },
      { name: "A/D Osc", val: latest.ado, bin: latest.binary_signals?.ADO },
      { name: "CCI", val: latest.cci, bin: latest.binary_signals?.CCI },
    ];

    grid.innerHTML = indicators
      .map((ind) => {
        const isUp = ind.bin === 1;
        const badgeColor = isUp
          ? "bg-emerald-950 text-emerald-400 border-emerald-800"
          : "bg-rose-950 text-rose-400 border-rose-800";
        const signText = isUp ? "+1 UP" : "-1 DOWN";

        return `
        <div class="bg-slate-900 border border-slate-800 p-3 rounded-xl shadow">
          <div class="flex items-center justify-between">
            <span class="text-xs text-slate-400 font-medium">${ind.name}</span>
            <span class="text-[10px] font-bold px-1.5 py-0.5 rounded border ${badgeColor}">${signText}</span>
          </div>
          <p class="text-sm font-bold text-white mt-1.5 font-mono">${ind.val !== null ? ind.val : "--"}</p>
        </div>
      `;
      })
      .join("");
  }

  // Render Indicator Historical Table
  function renderIndicatorTable() {
    if (!currentIndicatorsData) return;
    const tbody = document.getElementById("indicator-table-body");
    const tail = currentIndicatorsData.slice(-50).reverse();

    tbody.innerHTML = tail
      .map(
        (r) => `
      <tr class="hover:bg-slate-800/50">
        <td class="p-2 font-mono text-slate-400">${r.date}</td>
        <td class="p-2 font-bold text-white">${r.close}</td>
        <td class="p-2">${r.sma || "--"}</td>
        <td class="p-2">${r.wma || "--"}</td>
        <td class="p-2">${r.mom || "--"}</td>
        <td class="p-2">${r.stck || "--"}</td>
        <td class="p-2">${r.stcd || "--"}</td>
        <td class="p-2">${r.rsi || "--"}</td>
        <td class="p-2">${r.sig || "--"}</td>
        <td class="p-2">${r.lwr || "--"}</td>
        <td class="p-2">${r.ado || "--"}</td>
        <td class="p-2">${r.cci || "--"}</td>
      </tr>
    `
      )
      .join("");
  }

  // Render Binary Historical Heatmap Table
  function renderBinaryTable() {
    if (!currentIndicatorsData) return;
    const tbody = document.getElementById("binary-table-body");
    const tail = currentIndicatorsData.slice(-50).reverse();

    function renderCell(val) {
      if (val === 1) {
        return '<span class="inline-block w-8 py-0.5 rounded bg-emerald-950 text-emerald-400 font-bold border border-emerald-800">+1</span>';
      }
      return '<span class="inline-block w-8 py-0.5 rounded bg-rose-950 text-rose-400 font-bold border border-rose-800">-1</span>';
    }

    tbody.innerHTML = tail
      .map(
        (r) => `
      <tr class="hover:bg-slate-800/50">
        <td class="p-2 text-left font-mono text-slate-400">${r.date}</td>
        <td class="p-2">${renderCell(r.binary_signals?.SMA)}</td>
        <td class="p-2">${renderCell(r.binary_signals?.WMA)}</td>
        <td class="p-2">${renderCell(r.binary_signals?.MOM)}</td>
        <td class="p-2">${renderCell(r.binary_signals?.STCK)}</td>
        <td class="p-2">${renderCell(r.binary_signals?.STCD)}</td>
        <td class="p-2">${renderCell(r.binary_signals?.RSI)}</td>
        <td class="p-2">${renderCell(r.binary_signals?.SIG)}</td>
        <td class="p-2">${renderCell(r.binary_signals?.LWR)}</td>
        <td class="p-2">${renderCell(r.binary_signals?.ADO)}</td>
        <td class="p-2">${renderCell(r.binary_signals?.CCI)}</td>
      </tr>
    `
      )
      .join("");
  }

  // -----------------------------------------------------------------------
  // 4. Model Benchmarking Suite
  // -----------------------------------------------------------------------
  async function runModelBenchmark() {
    btnRunBenchmark.disabled = true;
    btnRunBenchmark.innerHTML = `<span class="spinner mr-2"></span> Benchmarking Models on GPU...`;

    const isTicker = ["AAPL", "NVDA", "MSFT", "TSLA", "SPY", "BTC-USD", "CL=F"].includes(
      sectorSelect.value
    ) || customTickerInput.value.trim() !== "";

    const payload = {
      sector_key: isTicker ? null : sectorSelect.value,
      ticker: isTicker ? (customTickerInput.value.trim().toUpperCase() || sectorSelect.value) : null,
      sequence_length: 20,
    };

    try {
      const res = await fetch("/api/benchmark", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });

      const data = await res.json();
      renderBenchmarkChart(data.continuous_results, data.binary_results);
      renderBenchmarkTable(data.continuous_results, data.binary_results);
    } catch (err) {
      console.error("Benchmark failed:", err);
    } finally {
      btnRunBenchmark.disabled = false;
      btnRunBenchmark.innerHTML = `<i data-lucide="play" class="w-4 h-4"></i><span>Execute Full Benchmark Suite</span>`;
      lucide.createIcons();
    }
  }

  function renderBenchmarkChart(contResults, binResults) {
    const ctx = document.getElementById("benchmark-chart").getContext("2d");
    const labels = contResults.map((r) => r.model_name);
    const contF1 = contResults.map((r) => r.f1_score);
    const binF1 = binResults.map((r) => r.f1_score);

    if (benchmarkChartInstance) {
      benchmarkChartInstance.destroy();
    }

    benchmarkChartInstance = new Chart(ctx, {
      type: "bar",
      data: {
        labels,
        datasets: [
          {
            label: "Continuous Data Representation",
            data: contF1,
            backgroundColor: "rgba(99, 102, 241, 0.8)",
            borderRadius: 6,
          },
          {
            label: "Binary Trend Representation (Paper Advancement)",
            data: binF1,
            backgroundColor: "rgba(16, 185, 129, 0.8)",
            borderRadius: 6,
          },
        ],
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: { labels: { color: "#cbd5e1" } },
          tooltip: {
            backgroundColor: "#0f172a",
            borderColor: "#334155",
            borderWidth: 1,
          },
        },
        scales: {
          x: {
            grid: { color: "#1e293b" },
            ticks: { color: "#94a3b8" },
          },
          y: {
            min: 0.4,
            max: 1.0,
            grid: { color: "#1e293b" },
            ticks: { color: "#94a3b8" },
            title: { display: true, text: "F1-Score", color: "#64748b" },
          },
        },
      },
    });
  }

  function renderBenchmarkTable(contResults, binResults) {
    const tbody = document.getElementById("benchmark-table-body");
    const combined = [];

    contResults.forEach((c) => {
      combined.push({ ...c, mode_label: "Continuous" });
    });
    binResults.forEach((b) => {
      combined.push({ ...b, mode_label: "Binary" });
    });

    tbody.innerHTML = combined
      .map((r) => {
        const modeBadge =
          r.mode_label === "Binary"
            ? '<span class="bg-emerald-950 text-emerald-400 border border-emerald-800 text-[10px] px-2 py-0.5 rounded font-bold">Binary</span>'
            : '<span class="bg-indigo-950 text-indigo-400 border border-indigo-800 text-[10px] px-2 py-0.5 rounded font-bold">Continuous</span>';

        return `
        <tr class="hover:bg-slate-800/50">
          <td class="p-2.5 font-semibold text-white">${r.model_name}</td>
          <td class="p-2.5 text-center">${modeBadge}</td>
          <td class="p-2.5 text-center font-bold font-mono text-emerald-400">${(r.f1_score * 100).toFixed(1)}%</td>
          <td class="p-2.5 text-center font-mono">${(r.accuracy * 100).toFixed(1)}%</td>
          <td class="p-2.5 text-center font-mono">${r.roc_auc.toFixed(3)}</td>
          <td class="p-2.5 text-center font-mono">${(r.precision * 100).toFixed(1)}%</td>
          <td class="p-2.5 text-center font-mono">${(r.recall * 100).toFixed(1)}%</td>
          <td class="p-2.5 text-center font-mono">${r.train_time_seconds}s</td>
          <td class="p-2.5 text-center font-mono text-slate-400">${r.latency_per_sample_us} &mu;s</td>
        </tr>
      `;
      })
      .join("");
  }

  // -----------------------------------------------------------------------
  // 5. Live Trend Prediction
  // -----------------------------------------------------------------------
  async function runLivePrediction() {
    btnRunPrediction.disabled = true;
    btnRunPrediction.innerHTML = `<span class="spinner mr-2"></span> Running Inference...`;

    const modelName = document.getElementById("predict-model-select").value;
    const mode = document.getElementById("predict-mode-select").value;

    const isTicker = ["AAPL", "NVDA", "MSFT", "TSLA", "SPY", "BTC-USD", "CL=F"].includes(
      sectorSelect.value
    ) || customTickerInput.value.trim() !== "";

    const ticker = isTicker
      ? customTickerInput.value.trim().toUpperCase() || sectorSelect.value
      : "sample";

    try {
      const res = await fetch("/api/predict", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          ticker,
          model_name: modelName,
          data_mode: mode,
        }),
      });

      const data = await res.json();
      const isUp = data.prediction_signal === 1;

      const iconWrapper = document.getElementById("trend-icon-wrapper");
      const trendText = document.getElementById("trend-text");
      const confSub = document.getElementById("confidence-subtext");
      const confUp = document.getElementById("conf-up-label");
      const confDown = document.getElementById("conf-down-label");
      const barUp = document.getElementById("conf-bar-up");
      const barDown = document.getElementById("conf-bar-down");

      if (isUp) {
        iconWrapper.className =
          "w-20 h-20 mx-auto rounded-full bg-emerald-950/80 border-2 border-emerald-500 flex items-center justify-center mb-3 shadow-lg shadow-emerald-500/20";
        iconWrapper.innerHTML = '<i data-lucide="trending-up" class="w-10 h-10 text-emerald-400"></i>';
        trendText.className = "text-3xl font-extrabold text-emerald-400 tracking-wide";
        trendText.textContent = "UPWARD TREND (+1)";
      } else {
        iconWrapper.className =
          "w-20 h-20 mx-auto rounded-full bg-rose-950/80 border-2 border-rose-500 flex items-center justify-center mb-3 shadow-lg shadow-rose-500/20";
        iconWrapper.innerHTML = '<i data-lucide="trending-down" class="w-10 h-10 text-rose-400"></i>';
        trendText.className = "text-3xl font-extrabold text-rose-400 tracking-wide";
        trendText.textContent = "DOWNWARD TREND (-1)";
      }

      confSub.textContent = `Model Confidence: ${data.confidence_up}% UP vs ${data.confidence_down}% DOWN`;
      confUp.textContent = `Up: ${data.confidence_up}%`;
      confDown.textContent = `Down: ${data.confidence_down}%`;
      barUp.style.width = `${data.confidence_up}%`;
      barDown.style.width = `${data.confidence_down}%`;

      lucide.createIcons();
    } catch (err) {
      console.error("Live prediction failed:", err);
    } finally {
      btnRunPrediction.disabled = false;
      btnRunPrediction.innerHTML = `<i data-lucide="sparkles" class="w-4 h-4"></i><span>Predict Trend Direction</span>`;
      lucide.createIcons();
    }
  }

  // -----------------------------------------------------------------------
  // 6. Strategy Backtesting
  // -----------------------------------------------------------------------
  async function runBacktesting() {
    btnRunBacktest.disabled = true;
    btnRunBacktest.innerHTML = `<span class="spinner mr-2"></span> Simulating Strategy Execution...`;

    const isTicker = ["AAPL", "NVDA", "MSFT", "TSLA", "SPY", "BTC-USD", "CL=F"].includes(
      sectorSelect.value
    ) || customTickerInput.value.trim() !== "";

    const payload = {
      model_name: "lstm",
      data_mode: "binary",
      sector_key: isTicker ? null : sectorSelect.value,
      ticker: isTicker ? (customTickerInput.value.trim().toUpperCase() || sectorSelect.value) : null,
      initial_capital: 100000.0,
      transaction_cost_pct: 0.001,
      allow_short: false,
    };

    try {
      const res = await fetch("/api/backtest", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });

      const data = await res.json();
      renderBacktestKPIs(data.metrics);
      renderEquityChart(data.equity_curve);
    } catch (err) {
      console.error("Backtest failed:", err);
    } finally {
      btnRunBacktest.disabled = false;
      btnRunBacktest.innerHTML = `<i data-lucide="play" class="w-4 h-4"></i><span>Run Strategy Simulation</span>`;
      lucide.createIcons();
    }
  }

  function renderBacktestKPIs(m) {
    const grid = document.getElementById("backtest-kpi-grid");
    const kpis = [
      {
        label: "Strategy Return",
        val: `+${m.strategy_total_return_pct}%`,
        sub: `Benchmark: +${m.benchmark_total_return_pct}%`,
        color: "text-emerald-400",
      },
      {
        label: "Sharpe Ratio",
        val: m.sharpe_ratio.toFixed(2),
        sub: `Sortino: ${m.sortino_ratio.toFixed(2)}`,
        color: "text-indigo-400",
      },
      {
        label: "Max Drawdown",
        val: `${m.max_drawdown_pct}%`,
        sub: `Bench MDD: ${m.benchmark_max_drawdown_pct}%`,
        color: "text-rose-400",
      },
      {
        label: "Win Rate & Trades",
        val: `${m.win_rate_pct}%`,
        sub: `${m.num_trades} Total Trades`,
        color: "text-amber-400",
      },
    ];

    grid.innerHTML = kpis
      .map(
        (k) => `
      <div class="bg-slate-900 border border-slate-800 p-4 rounded-2xl shadow-xl">
        <p class="text-xs text-slate-400 font-medium">${k.label}</p>
        <h4 class="text-xl font-extrabold ${k.color} my-1 font-mono">${k.val}</h4>
        <p class="text-[11px] text-slate-500 font-mono">${k.sub}</p>
      </div>
    `
      )
      .join("");
  }

  function renderEquityChart(eq) {
    const ctx = document.getElementById("equity-chart").getContext("2d");
    if (equityChartInstance) {
      equityChartInstance.destroy();
    }

    equityChartInstance = new Chart(ctx, {
      type: "line",
      data: {
        labels: eq.dates,
        datasets: [
          {
            label: "ML/DL Strategy Portfolio ($)",
            data: eq.strategy_wealth,
            borderColor: "#10b981",
            backgroundColor: "rgba(16, 185, 129, 0.1)",
            borderWidth: 2,
            fill: true,
            tension: 0.1,
          },
          {
            label: "Buy & Hold Benchmark ($)",
            data: eq.benchmark_wealth,
            borderColor: "#64748b",
            borderWidth: 1.5,
            borderDash: [3, 3],
            fill: false,
            tension: 0.1,
          },
        ],
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        interaction: { mode: "index", intersect: false },
        plugins: {
          legend: { labels: { color: "#cbd5e1" } },
          tooltip: {
            backgroundColor: "#0f172a",
            borderColor: "#334155",
            borderWidth: 1,
          },
        },
        scales: {
          x: {
            grid: { color: "#1e293b" },
            ticks: { color: "#64748b", maxTicksLimit: 12 },
          },
          y: {
            grid: { color: "#1e293b" },
            ticks: { color: "#64748b" },
          },
        },
      },
    });
  }

  // -----------------------------------------------------------------------
  // Event Listeners & Bootstrapping
  // -----------------------------------------------------------------------
  sectorSelect.addEventListener("change", () => {
    customTickerInput.value = "";
    loadMarketAndIndicators();
  });

  btnCustomTicker.addEventListener("click", loadMarketAndIndicators);
  customTickerInput.addEventListener("keypress", (e) => {
    if (e.key === "Enter") loadMarketAndIndicators();
  });

  btnRefreshData.addEventListener("click", loadMarketAndIndicators);
  overlaySelect.addEventListener("change", renderPriceChart);

  btnRunBenchmark.addEventListener("click", runModelBenchmark);
  btnRunPrediction.addEventListener("click", runLivePrediction);
  btnRunBacktest.addEventListener("click", runBacktesting);

  // Initial Load
  checkSystemStatus();
  loadMarketAndIndicators();
});
