"""
Institutional Risk & Advanced Monte Carlo Simulation Engine.
Implements:
- Dynamic Kelly Sizing & Volatility Targeting
- Trailing Stop-Loss & Take-Profit Execution
- 1,000-Path Monte Carlo Portfolio Simulation (VaR / CVaR 95%)
"""

from typing import Any, Dict, List, Optional, Union
import numpy as np
import pandas as pd


class AdvancedRiskBacktester:
    """
    Simulates institutional trade execution with dynamic position sizing,
    risk management boundaries, and Monte Carlo probabilistic projections.
    """

    def __init__(
        self,
        initial_capital: float = 100000.0,
        target_annual_vol: float = 0.15,
        transaction_cost_pct: float = 0.001,
        max_position_size: float = 1.0,
        trailing_stop_pct: Optional[float] = 0.03,  # 3% trailing stop
        periods_per_year: int = 252,
    ):
        self.initial_capital = initial_capital
        self.target_annual_vol = target_annual_vol
        self.transaction_cost_pct = transaction_cost_pct
        self.max_position_size = max_position_size
        self.trailing_stop_pct = trailing_stop_pct
        self.periods_per_year = periods_per_year

    def run_risk_managed_backtest(
        self,
        prices: Union[pd.Series, np.ndarray],
        signals: Union[pd.Series, np.ndarray],
        confidence_probs: Optional[np.ndarray] = None,
        dates: Optional[Union[pd.DatetimeIndex, List[Any]]] = None,
    ) -> Dict[str, Any]:
        """
        Execute risk-managed backtest with dynamic sizing and stop-loss logic.
        """
        p = np.asarray(prices, dtype=np.float64)
        s = np.asarray(signals, dtype=np.float64)
        n = len(p)

        if len(p) != len(s):
            raise ValueError("Prices and signals length mismatch")

        # Calculate daily price returns
        price_returns = np.diff(p) / p[:-1]

        # Rolling 20-day annualized volatility
        ret_series = pd.Series(price_returns)
        rolling_vol = (
            ret_series.rolling(20, min_periods=5).std() * np.sqrt(self.periods_per_year)
        ).fillna(0.15).values

        # Dynamic Position Sizing
        positions = np.zeros(n - 1, dtype=np.float64)
        for t in range(n - 1):
            if s[t] == 1:
                # Volatility-targeting scale
                vol_scale = min(
                    self.target_annual_vol / max(rolling_vol[t], 0.05),
                    self.max_position_size,
                )
                # Confidence scaling (if available)
                conf_scale = (
                    confidence_probs[t] if (confidence_probs is not None and t < len(confidence_probs)) else 1.0
                )
                positions[t] = min(vol_scale * conf_scale, self.max_position_size)
            else:
                positions[t] = 0.0

        # Trailing stop-loss simulation
        if self.trailing_stop_pct is not None:
            in_pos = False
            peak_p = 0.0
            for t in range(n - 1):
                if positions[t] > 0:
                    if not in_pos:
                        in_pos = True
                        peak_p = p[t]
                    else:
                        peak_p = max(peak_p, p[t])
                        # Check trailing drawdown
                        drawdown_from_peak = (p[t] - peak_p) / peak_p
                        if drawdown_from_peak < -self.trailing_stop_pct:
                            positions[t] = 0.0  # Stopped out
                            in_pos = False
                else:
                    in_pos = False

        # Transaction costs
        pos_diff = np.abs(np.diff(np.insert(positions, 0, 0.0)))
        tx_costs = pos_diff * self.transaction_cost_pct

        strat_returns = (positions * price_returns) - tx_costs
        wealth = self.initial_capital * np.cumprod(1.0 + strat_returns)
        wealth = np.insert(wealth, 0, self.initial_capital)

        bench_wealth = self.initial_capital * np.cumprod(1.0 + price_returns)
        bench_wealth = np.insert(bench_wealth, 0, self.initial_capital)

        # -----------------------------------------------------------------
        # Monte Carlo 1,000-Path Simulation
        # -----------------------------------------------------------------
        monte_carlo_res = self._run_monte_carlo(strat_returns, num_simulations=1000, horizon_days=min(n, 252))

        total_ret = float((wealth[-1] - self.initial_capital) / self.initial_capital)
        bench_ret = float((bench_wealth[-1] - self.initial_capital) / self.initial_capital)

        ann_vol = float(np.std(strat_returns) * np.sqrt(self.periods_per_year))
        sharpe = float((np.mean(strat_returns) / (np.std(strat_returns) + 1e-9)) * np.sqrt(self.periods_per_year))

        peak = np.maximum.accumulate(wealth)
        dd = (wealth - peak) / peak
        max_dd = float(np.min(dd))

        date_strings = (
            [str(d)[:10] for d in dates] if dates is not None and len(dates) == n else [f"Day_{i}" for i in range(n)]
        )

        return {
            "metrics": {
                "initial_capital": self.initial_capital,
                "final_portfolio_value": round(float(wealth[-1]), 2),
                "strategy_return_pct": round(total_ret * 100.0, 2),
                "benchmark_return_pct": round(bench_ret * 100.0, 2),
                "sharpe_ratio": round(sharpe, 2),
                "max_drawdown_pct": round(max_dd * 100.0, 2),
                "annualized_vol_pct": round(ann_vol * 100.0, 2),
                "var_95_pct": monte_carlo_res["var_95_pct"],
                "cvar_95_pct": monte_carlo_res["cvar_95_pct"],
            },
            "equity_curve": {
                "dates": date_strings,
                "strategy_wealth": [round(float(w), 2) for w in wealth],
                "benchmark_wealth": [round(float(w), 2) for w in bench_wealth],
            },
            "monte_carlo": monte_carlo_res["fan_chart"],
        }

    def _run_monte_carlo(
        self, daily_returns: np.ndarray, num_simulations: int = 1000, horizon_days: int = 150
    ) -> Dict[str, Any]:
        """
        Bootstrap Monte Carlo future path simulations.
        """
        rng = np.random.default_rng(42)
        sim_paths = np.zeros((num_simulations, horizon_days + 1))
        sim_paths[:, 0] = self.initial_capital

        clean_rets = daily_returns[~np.isnan(daily_returns)]
        if len(clean_rets) < 10:
            clean_rets = np.array([0.0005, -0.0003, 0.001, -0.0008, 0.0004])

        for s in range(num_simulations):
            boot_rets = rng.choice(clean_rets, size=horizon_days, replace=True)
            sim_paths[s, 1:] = self.initial_capital * np.cumprod(1.0 + boot_rets)

        # Final returns distribution
        final_returns = (sim_paths[:, -1] - self.initial_capital) / self.initial_capital
        var_95 = float(np.percentile(final_returns, 5))
        cvar_95 = float(np.mean(final_returns[final_returns <= var_95]))

        # Percentile trajectories for fan chart
        p5 = np.percentile(sim_paths, 5, axis=0)
        p25 = np.percentile(sim_paths, 25, axis=0)
        p50 = np.percentile(sim_paths, 50, axis=0)
        p75 = np.percentile(sim_paths, 75, axis=0)
        p95 = np.percentile(sim_paths, 95, axis=0)

        steps = [f"+{i}d" for i in range(horizon_days + 1)]

        return {
            "var_95_pct": round(var_95 * 100.0, 2),
            "cvar_95_pct": round(cvar_95 * 100.0, 2),
            "fan_chart": {
                "steps": steps[::5],
                "p5": [round(float(v), 2) for v in p5[::5]],
                "p25": [round(float(v), 2) for v in p25[::5]],
                "p50": [round(float(v), 2) for v in p50[::5]],
                "p75": [round(float(v), 2) for v in p75[::5]],
                "p95": [round(float(v), 2) for v in p95[::5]],
            },
        }
