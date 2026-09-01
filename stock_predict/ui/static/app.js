/**
 * StockTrend AI - Next-Gen Quantitative Intelligence Dashboard Client
 */

document.addEventListener("DOMContentLoaded", () => {
  lucide.createIcons();

  // State
  let currentIndicatorsData = null;
  let priceChartInstance = null;
  let benchmarkChartInstance = null;
  let equityChartInstance = null;
  let multiHorizonChartInstance = null;
  let featureImportanceChartInstance = null;
  let temporalAttentionChartInstance = null;
  let monteCarloChartInstance = null;

  // DOM Elements
  const tabBtns = document.querySelectorAll(".tab-btn");
  const tabContents = document.querySelectorAll(".tab-content");
  const sectorSelect = document.getElementById("sector-select");
  const customTickerInput = document.getElementById("custom-ticker-input");
  const btnCustomTicker = document.getElementById("btn-custom-ticker");
  const btnRefreshData = document.getElementById("btn-refresh-data");
  const overlaySelect = document.getElementById("indicator-overlay-select");

  const btnRunMultiHorizon = document.getElementById("btn-run-multi-horizon");
  const btnRunExplain = document.getElementById("btn-run-explain");
  const btnRunMonteCarlo = document.getElementById("btn-run-monte-carlo");
  const btnRunBenchmark = document.getElementById("btn-run-benchmark");
  const btnRunPrediction = document.getElementById("btn-run-prediction");
  const btnRunBacktest = document.getElementById("btn-run-backtest");

  // -----------------------------------------------------------------------
  // 1. Tab Navigation
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
  // 2. Hardware Diagnostics
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

  function getTargetParams() {
    const isTicker = ["AAPL", "NVDA", "MSFT", "TSLA", "SPY", "BTC-USD", "CL=F"].includes(
      sectorSelect.value
    ) || customTickerInput.value.trim() !== "";

    if (customTickerInput.value.trim() !== "") {
      return { source: "ticker", ticker: customTickerInput.value.trim().toUpperCase() };
    } else if (isTicker) {
      return { source: "ticker", ticker: sectorSelect.value };
    }
    return { source: "sample", sector_key: sectorSelect.value };
  }

  // -----------------------------------------------------------------------
  // 3. Technical Indicators & Price Chart
  // -----------------------------------------------------------------------
  async function loadMarketAndIndicators() {
    const payload = getTargetParams();
    const assetName = payload.ticker || sectorSelect.options[sectorSelect.selectedIndex].text;
    document.getElementById("asset-subtitle").textContent = `${assetName} Historical Series`;
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
    } catch (err) {
      console.error("Failed to load indicators:", err);
    }
  }

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

    priceChartInstance = new Chart(ctx, {
      type: "line",
      data: {
        labels,
        datasets: [
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
        ],
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        interaction: { mode: "index", intersect: false },
        plugins: {
          legend: { labels: { color: "#94a3b8" } },
          tooltip: { backgroundColor: "#0f172a", borderColor: "#334155", borderWidth: 1 },
        },
        scales: {
          x: { grid: { color: "#1e293b" }, ticks: { color: "#64748b", maxTicksLimit: 12 } },
          y: { position: "left", grid: { color: "#1e293b" }, ticks: { color: "#64748b" } },
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

  // -----------------------------------------------------------------------
  // 4. Multi-Horizon Forecasting (1D, 3D, 5D, 10D, 20D)
  // -----------------------------------------------------------------------
  async function runMultiHorizon() {
    btnRunMultiHorizon.disabled = true;
    btnRunMultiHorizon.innerHTML = `<span class="spinner mr-2"></span> Forecasting on GPU...`;

    const target = getTargetParams();
    const payload = {
      ticker: target.ticker || "sample",
      model_name: "tft",
      data_mode: "binary",
    };

    try {
      const res = await fetch("/api/predict/multi-horizon", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });
      const data = await res.json();
      renderMultiHorizonGrid(data.forecasts);
      renderMultiHorizonChart(data.forecasts);
    } catch (err) {
      console.error("Multi-horizon forecast failed:", err);
    } finally {
      btnRunMultiHorizon.disabled = false;
      btnRunMultiHorizon.innerHTML = `<i data-lucide="sparkles" class="w-4 h-4"></i><span>Compute Multi-Horizon Forecasts</span>`;
      lucide.createIcons();
    }
  }

  function renderMultiHorizonGrid(fcasts) {
    const grid = document.getElementById("multi-horizon-grid");
    const horizons = Object.keys(fcasts);

    grid.innerHTML = horizons
      .map((k) => {
        const item = fcasts[k];
        const isUp = item.trend === "UP";
        const badgeColor = isUp ? "text-emerald-400 bg-emerald-950/80 border-emerald-800" : "text-rose-400 bg-rose-950/80 border-rose-800";
        const icon = isUp ? "trending-up" : "trending-down";
        const returnSign = item.expected_return_pct >= 0 ? "+" : "";

        return `
        <div class="bg-slate-900 border border-slate-800 p-4 rounded-2xl shadow-xl flex flex-col justify-between">
          <div class="flex items-center justify-between mb-2">
            <span class="text-xs uppercase font-bold text-slate-400">${item.horizon_days}-Day Horizon</span>
            <span class="text-[10px] font-extrabold px-2 py-0.5 rounded border ${badgeColor}">${item.trend}</span>
          </div>
          <div class="my-2">
            <p class="text-2xl font-black ${isUp ? "text-emerald-400" : "text-rose-400"} font-mono">${returnSign}${item.expected_return_pct}%</p>
            <p class="text-[11px] text-slate-400">Expected Magnitude</p>
          </div>
          <div class="mt-2 space-y-1">
            <div class="flex justify-between text-[10px] text-slate-400">
              <span>Up: ${item.confidence_up_pct}%</span>
              <span>Down: ${item.confidence_down_pct}%</span>
            </div>
            <div class="w-full bg-rose-950 h-2 rounded-full overflow-hidden flex">
              <div class="bg-emerald-500 h-full" style="width: ${item.confidence_up_pct}%;"></div>
              <div class="bg-rose-500 h-full" style="width: ${item.confidence_down_pct}%;"></div>
            </div>
          </div>
        </div>
      `;
      })
      .join("");
    lucide.createIcons();
  }

  function renderMultiHorizonChart(fcasts) {
    const ctx = document.getElementById("multi-horizon-chart").getContext("2d");
    const horizons = Object.values(fcasts);
    const labels = horizons.map((h) => `${h.horizon_days}-Day`);
    const returns = horizons.map((h) => h.expected_return_pct);

    if (multiHorizonChartInstance) multiHorizonChartInstance.destroy();

    multiHorizonChartInstance = new Chart(ctx, {
      type: "bar",
      data: {
        labels,
        datasets: [
          {
            label: "Expected Forward Return (%)",
            data: returns,
            backgroundColor: returns.map((r) => (r >= 0 ? "rgba(16, 185, 129, 0.85)" : "rgba(244, 63, 94, 0.85)")),
            borderRadius: 6,
          },
        ],
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: { legend: { labels: { color: "#cbd5e1" } } },
        scales: {
          x: { grid: { color: "#1e293b" }, ticks: { color: "#94a3b8" } },
          y: { grid: { color: "#1e293b" }, ticks: { color: "#94a3b8" } },
        },
      },
    });
  }

  // -----------------------------------------------------------------------
  // 5. Explainable AI (XAI)
  // -----------------------------------------------------------------------
  async function runExplainability() {
    btnRunExplain.disabled = true;
    btnRunExplain.innerHTML = `<span class="spinner mr-2"></span> Extracting Gradients...`;

    const target = getTargetParams();
    const payload = {
      ticker: target.ticker || "sample",
      model_name: "tft",
      data_mode: "binary",
    };

    try {
      const res = await fetch("/api/explain", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });
      const data = await res.json();
      renderFeatureImportance(data.explanation.feature_importance);
      renderTemporalAttention(data.explanation.temporal_weights);
    } catch (err) {
      console.error("Explainability extraction failed:", err);
    } finally {
      btnRunExplain.disabled = false;
      btnRunExplain.innerHTML = `<i data-lucide="search" class="w-4 h-4"></i><span>Extract Model Attribution</span>`;
      lucide.createIcons();
    }
  }

  function renderFeatureImportance(featImp) {
    const ctx = document.getElementById("feature-importance-chart").getContext("2d");
    const labels = featImp.map((f) => f.name);
    const data = featImp.map((f) => f.importance_pct);

    if (featureImportanceChartInstance) featureImportanceChartInstance.destroy();

    featureImportanceChartInstance = new Chart(ctx, {
      type: "bar",
      data: {
        labels,
        datasets: [
          {
            label: "Attribution Score (%)",
            data,
            backgroundColor: "rgba(168, 85, 247, 0.85)",
            borderRadius: 6,
          },
        ],
      },
      options: {
        indexAxis: "y",
        responsive: true,
        maintainAspectRatio: false,
        plugins: { legend: { labels: { color: "#cbd5e1" } } },
        scales: {
          x: { grid: { color: "#1e293b" }, ticks: { color: "#94a3b8" } },
          y: { grid: { color: "#1e293b" }, ticks: { color: "#94a3b8" } },
        },
      },
    });
  }

  function renderTemporalAttention(tempWeights) {
    const ctx = document.getElementById("temporal-attention-chart").getContext("2d");
    const labels = tempWeights.map((_, i) => `t-${tempWeights.length - i}`);

    if (temporalAttentionChartInstance) temporalAttentionChartInstance.destroy();

    temporalAttentionChartInstance = new Chart(ctx, {
      type: "line",
      data: {
        labels,
        datasets: [
          {
            label: "Temporal Attention Weight",
            data: tempWeights,
            borderColor: "#a855f7",
            backgroundColor: "rgba(168, 85, 247, 0.2)",
            borderWidth: 2,
            fill: true,
            tension: 0.3,
          },
        ],
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: { legend: { labels: { color: "#cbd5e1" } } },
        scales: {
          x: { grid: { color: "#1e293b" }, ticks: { color: "#94a3b8" } },
          y: { grid: { color: "#1e293b" }, ticks: { color: "#94a3b8" } },
        },
      },
    });
  }

  // -----------------------------------------------------------------------
  // 6. Monte Carlo 1,000-Path Simulation
  // -----------------------------------------------------------------------
  async function runMonteCarlo() {
    btnRunMonteCarlo.disabled = true;
    btnRunMonteCarlo.innerHTML = `<span class="spinner mr-2"></span> Simulating 1,000 Paths...`;

    const target = getTargetParams();
    const payload = {
      model_name: "tcn",
      data_mode: "binary",
      sector_key: target.sector_key || null,
      ticker: target.ticker || null,
      initial_capital: 100000.0,
      transaction_cost_pct: 0.001,
    };

    try {
      const res = await fetch("/api/backtest/monte-carlo", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });
      const data = await res.json();
      renderMonteCarloKPIs(data.metrics);
      renderMonteCarloChart(data.monte_carlo);
    } catch (err) {
      console.error("Monte Carlo simulation failed:", err);
    } finally {
      btnRunMonteCarlo.disabled = false;
      btnRunMonteCarlo.innerHTML = `<i data-lucide="play" class="w-4 h-4"></i><span>Simulate 1,000 Monte Carlo Paths</span>`;
      lucide.createIcons();
    }
  }

  function renderMonteCarloKPIs(m) {
    const grid = document.getElementById("monte-carlo-kpis");
    const kpis = [
      { label: "Final Portfolio Value", val: `$${m.final_portfolio_value.toLocaleString()}`, color: "text-emerald-400" },
      { label: "Strategy Return", val: `+${m.strategy_return_pct}%`, color: "text-emerald-400" },
      { label: "95% Value at Risk (VaR)", val: `${m.var_95_pct}%`, color: "text-amber-400" },
      { label: "95% Expected Shortfall (CVaR)", val: `${m.cvar_95_pct}%`, color: "text-rose-400" },
    ];

    grid.innerHTML = kpis
      .map(
        (k) => `
      <div class="bg-slate-900 border border-slate-800 p-4 rounded-2xl shadow-xl">
        <p class="text-xs text-slate-400 font-medium">${k.label}</p>
        <h4 class="text-xl font-extrabold ${k.color} my-1 font-mono">${k.val}</h4>
      </div>
    `
      )
      .join("");
  }

  function renderMonteCarloChart(fan) {
    const ctx = document.getElementById("monte-carlo-chart").getContext("2d");
    if (monteCarloChartInstance) monteCarloChartInstance.destroy();

    monteCarloChartInstance = new Chart(ctx, {
      type: "line",
      data: {
        labels: fan.steps,
        datasets: [
          { label: "95th Percentile", data: fan.p95, borderColor: "#10b981", borderWidth: 1.5, fill: false },
          { label: "75th Percentile", data: fan.p75, borderColor: "#34d399", borderWidth: 1.2, fill: false },
          { label: "Median Path (50th)", data: fan.p50, borderColor: "#6366f1", borderWidth: 2.5, fill: false },
          { label: "25th Percentile", data: fan.p25, borderColor: "#f43f5e", borderWidth: 1.2, fill: false },
          { label: "5th Percentile (VaR)", data: fan.p5, borderColor: "#e11d48", borderWidth: 1.5, fill: false },
        ],
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: { legend: { labels: { color: "#cbd5e1" } } },
        scales: {
          x: { grid: { color: "#1e293b" }, ticks: { color: "#94a3b8" } },
          y: { grid: { color: "#1e293b" }, ticks: { color: "#94a3b8" } },
        },
      },
    });
  }

  // -----------------------------------------------------------------------
  // 7. Model Benchmarking
  // -----------------------------------------------------------------------
  async function runModelBenchmark() {
    btnRunBenchmark.disabled = true;
    btnRunBenchmark.innerHTML = `<span class="spinner mr-2"></span> Benchmarking 15 Models on GPU...`;
    const target = getTargetParams();

    try {
      const res = await fetch("/api/benchmark", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          sector_key: target.sector_key || null,
          ticker: target.ticker || null,
          sequence_length: 20,
        }),
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

    if (benchmarkChartInstance) benchmarkChartInstance.destroy();

    benchmarkChartInstance = new Chart(ctx, {
      type: "bar",
      data: {
        labels,
        datasets: [
          { label: "Continuous [0, 1]", data: contF1, backgroundColor: "rgba(99, 102, 241, 0.8)", borderRadius: 6 },
          { label: "Binary Trend (+1/-1)", data: binF1, backgroundColor: "rgba(16, 185, 129, 0.8)", borderRadius: 6 },
        ],
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: { legend: { labels: { color: "#cbd5e1" } } },
        scales: {
          x: { grid: { color: "#1e293b" }, ticks: { color: "#94a3b8" } },
          y: { min: 0.4, max: 1.0, grid: { color: "#1e293b" }, ticks: { color: "#94a3b8" } },
        },
      },
    });
  }

  function renderBenchmarkTable(contResults, binResults) {
    const tbody = document.getElementById("benchmark-table-body");
    const combined = [];
    contResults.forEach((c) => combined.push({ ...c, mode_label: "Continuous" }));
    binResults.forEach((b) => combined.push({ ...b, mode_label: "Binary" }));

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
        </tr>
      `;
      })
      .join("");
  }

  // -----------------------------------------------------------------------
  // 8. Live Trend Prediction
  // -----------------------------------------------------------------------
  async function runLivePrediction() {
    btnRunPrediction.disabled = true;
    btnRunPrediction.innerHTML = `<span class="spinner mr-2"></span> Running Inference...`;

    const modelName = document.getElementById("predict-model-select").value;
    const mode = document.getElementById("predict-mode-select").value;
    const target = getTargetParams();

    try {
      const res = await fetch("/api/predict", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          ticker: target.ticker || "sample",
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
        iconWrapper.className = "w-20 h-20 mx-auto rounded-full bg-emerald-950/80 border-2 border-emerald-500 flex items-center justify-center mb-3 shadow-lg shadow-emerald-500/20";
        iconWrapper.innerHTML = '<i data-lucide="trending-up" class="w-10 h-10 text-emerald-400"></i>';
        trendText.className = "text-3xl font-extrabold text-emerald-400 tracking-wide";
        trendText.textContent = "UPWARD TREND (+1)";
      } else {
        iconWrapper.className = "w-20 h-20 mx-auto rounded-full bg-rose-950/80 border-2 border-rose-500 flex items-center justify-center mb-3 shadow-lg shadow-rose-500/20";
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
  // 9. Strategy Backtest
  // -----------------------------------------------------------------------
  async function runBacktesting() {
    btnRunBacktest.disabled = true;
    btnRunBacktest.innerHTML = `<span class="spinner mr-2"></span> Simulating Strategy...`;
    const target = getTargetParams();

    try {
      const res = await fetch("/api/backtest", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          model_name: "tcn",
          data_mode: "binary",
          sector_key: target.sector_key || null,
          ticker: target.ticker || null,
          initial_capital: 100000.0,
          transaction_cost_pct: 0.001,
          allow_short: false,
        }),
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
      { label: "Strategy Return", val: `+${m.strategy_total_return_pct}%`, sub: `Benchmark: +${m.benchmark_total_return_pct}%`, color: "text-emerald-400" },
      { label: "Sharpe Ratio", val: m.sharpe_ratio.toFixed(2), sub: `Sortino: ${m.sortino_ratio.toFixed(2)}`, color: "text-indigo-400" },
      { label: "Max Drawdown", val: `${m.max_drawdown_pct}%`, sub: `Bench MDD: ${m.benchmark_max_drawdown_pct}%`, color: "text-rose-400" },
      { label: "Win Rate & Trades", val: `${m.win_rate_pct}%`, sub: `${m.num_trades} Total Trades`, color: "text-amber-400" },
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
    if (equityChartInstance) equityChartInstance.destroy();

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
        plugins: { legend: { labels: { color: "#cbd5e1" } } },
        scales: {
          x: { grid: { color: "#1e293b" }, ticks: { color: "#64748b", maxTicksLimit: 12 } },
          y: { grid: { color: "#1e293b" }, ticks: { color: "#64748b" } },
        },
      },
    });
  }

  // -----------------------------------------------------------------------
  // Event Listeners
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

  btnRunMultiHorizon.addEventListener("click", runMultiHorizon);
  btnRunExplain.addEventListener("click", runExplainability);
  btnRunMonteCarlo.addEventListener("click", runMonteCarlo);
  btnRunBenchmark.addEventListener("click", runModelBenchmark);
  btnRunPrediction.addEventListener("click", runLivePrediction);
  btnRunBacktest.addEventListener("click", runBacktesting);

  // Bootstrap
  checkSystemStatus();
  loadMarketAndIndicators();
});
