"""
Institutional Virtual Paper-Trading Execution Ledger & Real-Time Portfolio Engine.
Features:
1. Multi-currency portfolio tracking ($ USD and ₹ INR).
2. Live Mark-to-Market (MTM) automated PnL updates.
3. Automated Stop-Loss (1.8x ATR) and Take-Profit (2.2x / 3.8x ATR) trigger execution.
4. Realistic execution slippage and exchange commission modeling.
5. Persistent JSON state on disk (data_storage/paper_portfolio.json).
"""

from typing import Any, Dict, List, Optional
import os
import json
import time
from datetime import datetime
import pandas as pd

PORTFOLIO_FILE = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
    "data_storage",
    "paper_portfolio.json",
)


class PaperTradingEngine:
    """
    Automated virtual paper-trading ledger and real-time execution engine.
    """

    def __init__(
        self,
        initial_cash_usd: float = 100_000.0,
        initial_cash_inr: float = 1_000_000.0,
        portfolio_file: Optional[str] = None,
    ):
        self.initial_cash_usd = initial_cash_usd
        self.initial_cash_inr = initial_cash_inr
        self.portfolio_file = portfolio_file or PORTFOLIO_FILE
        self._load_or_initialize()

    @property
    def trade_history(self) -> List[Dict[str, Any]]:
        return self.history

    def _load_or_initialize(self) -> None:
        os.makedirs(os.path.dirname(self.portfolio_file), exist_ok=True)
        if os.path.exists(self.portfolio_file):
            try:
                with open(self.portfolio_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self.cash_usd = data.get("cash_usd", self.initial_cash_usd)
                    self.cash_inr = data.get("cash_inr", self.initial_cash_inr)
                    self.positions = data.get("positions", {})
                    self.history = data.get("history", [])
                    return
            except Exception:
                pass

        self.cash_usd = self.initial_cash_usd
        self.cash_inr = self.initial_cash_inr
        self.positions = {}
        self.history = []
        self._save()

    def _save(self) -> None:
        data = {
            "cash_usd": round(self.cash_usd, 2),
            "cash_inr": round(self.cash_inr, 2),
            "positions": self.positions,
            "history": self.history,
            "last_updated": time.strftime("%Y-%m-%d %H:%M:%S"),
        }
        with open(self.portfolio_file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

    def _get_currency(self, ticker: str) -> str:
        clean = ticker.upper()
        return "₹" if (".NS" in clean or clean.startswith("^NSE") or "INR" in clean) else "$"

    def execute_order(
        self,
        ticker: str,
        action: str,  # "BUY" or "SELL" (Short)
        quantity: int,
        current_price: float,
        stop_loss: Optional[float] = None,
        take_profit: Optional[float] = None,
        notes: str = "Manual Paper Order",
    ) -> Dict[str, Any]:
        """
        Execute paper order with simulated slippage (0.03%) and commission.
        """
        clean = ticker.strip().upper()
        currency = self._get_currency(clean)
        is_inr = currency == "₹"

        # Apply realistic execution slippage
        slippage_pct = 0.0003  # 0.03%
        fill_price = round(
            current_price * (1.0 + slippage_pct) if action == "BUY" else current_price * (1.0 - slippage_pct),
            2,
        )
        total_cost = round(fill_price * quantity, 2)
        commission = 1.0 if not is_inr else 20.0  # $1 or ₹20 broker fee

        # Check funds if buying
        if action == "BUY":
            available = self.cash_inr if is_inr else self.cash_usd
            if total_cost + commission > available:
                return {
                    "success": False,
                    "message": f"Insufficient paper funds. Required {currency}{total_cost + commission:,.2f}, Available: {currency}{available:,.2f}",
                }
            if is_inr:
                self.cash_inr -= (total_cost + commission)
            else:
                self.cash_usd -= (total_cost + commission)

        trade_id = f"TRADE_{int(time.time() * 1000) % 1_000_000}"
        pos_key = clean

        # Record position
        self.positions[pos_key] = {
            "trade_id": trade_id,
            "ticker": clean,
            "action": action,
            "quantity": quantity,
            "entry_price": fill_price,
            "current_price": fill_price,
            "cost_basis": total_cost,
            "currency": currency,
            "stop_loss": stop_loss,
            "take_profit": take_profit,
            "entry_time": time.strftime("%Y-%m-%d %H:%M:%S"),
            "unrealized_pnl": 0.0,
            "unrealized_pnl_pct": 0.0,
            "notes": notes,
        }

        self._save()
        return {
            "success": True,
            "status": "FILLED",
            "trade_id": trade_id,
            "message": f"Executed {action} {quantity:,} shares of {clean} @ {currency}{fill_price:,.2f} (Slippage: {currency}{abs(fill_price - current_price):.2f})",
        }

    def close_position(self, ticker: str, current_price: float, reason: str = "Manual Exit") -> Dict[str, Any]:
        clean = ticker.strip().upper()
        if clean not in self.positions:
            return {"success": False, "message": f"No open position found for {clean}."}

        pos = self.positions.pop(clean)
        currency = pos["currency"]
        is_inr = currency == "₹"
        qty = pos["quantity"]
        entry_p = pos["entry_price"]
        action = pos["action"]

        # Slippage on exit
        slippage_pct = 0.0003
        exit_p = round(
            current_price * (1.0 - slippage_pct) if action == "BUY" else current_price * (1.0 + slippage_pct),
            2,
        )
        commission = 1.0 if not is_inr else 20.0

        if action == "BUY":
            gross_pnl = (exit_p - entry_p) * qty
            proceeds = (exit_p * qty) - commission
        else:
            gross_pnl = (entry_p - exit_p) * qty
            proceeds = pos["cost_basis"] + gross_pnl - commission

        net_pnl = round(gross_pnl - commission, 2)
        pnl_pct = round((net_pnl / pos["cost_basis"]) * 100.0, 2)

        if is_inr:
            self.cash_inr += proceeds
        else:
            self.cash_usd += proceeds

        # Log into history
        hist_entry = {
            "trade_id": pos["trade_id"],
            "ticker": clean,
            "action": action,
            "quantity": qty,
            "entry_price": entry_p,
            "exit_price": exit_p,
            "entry_time": pos["entry_time"],
            "exit_time": time.strftime("%Y-%m-%d %H:%M:%S"),
            "net_pnl": net_pnl,
            "pnl_pct": pnl_pct,
            "currency": currency,
            "reason": reason,
            "is_win": net_pnl > 0,
        }
        self.history.insert(0, hist_entry)
        self._save()

        return {
            "success": True,
            "status": "CLOSED",
            "message": f"Closed {clean} @ {currency}{exit_p:,.2f} | Net PnL: {currency}{net_pnl:+,.2f} ({pnl_pct:+.2f}%) | Reason: {reason}",
            "net_pnl": net_pnl,
        }

    def mark_to_market(self, prices_dict: Dict[str, float]) -> List[str]:
        """
        Update unrealized PnL for all active positions and auto-trigger SL/TP.
        Returns list of triggered closure notices.
        """
        notices = []
        to_close = []

        for ticker, pos in list(self.positions.items()):
            curr_p = prices_dict.get(ticker, pos["current_price"])
            pos["current_price"] = curr_p
            entry_p = pos["entry_price"]
            qty = pos["quantity"]
            action = pos["action"]
            sl = pos.get("stop_loss")
            tp = pos.get("take_profit")

            if action == "BUY":
                unrealized = (curr_p - entry_p) * qty
                # Check automated triggers
                if sl and curr_p <= sl:
                    to_close.append((ticker, curr_p, f"STOP-LOSS TRIGGERED ({pos['currency']}{sl:,.2f})"))
                elif tp and curr_p >= tp:
                    to_close.append((ticker, curr_p, f"TAKE-PROFIT TRIGGERED ({pos['currency']}{tp:,.2f})"))
            else:
                unrealized = (entry_p - curr_p) * qty
                if sl and curr_p >= sl:
                    to_close.append((ticker, curr_p, f"STOP-LOSS TRIGGERED ({pos['currency']}{sl:,.2f})"))
                elif tp and curr_p <= tp:
                    to_close.append((ticker, curr_p, f"TAKE-PROFIT TRIGGERED ({pos['currency']}{tp:,.2f})"))

            pos["unrealized_pnl"] = round(unrealized, 2)
            pos["unrealized_pnl_pct"] = round((unrealized / max(pos["cost_basis"], 1e-6)) * 100.0, 2)

        for ticker, price, reason in to_close:
            res = self.close_position(ticker, price, reason=reason)
            notices.append(res["message"])

        self._save()
        return notices

    def get_summary(self) -> Dict[str, Any]:
        """
        Compile complete portfolio overview, metrics, positions table, and history table.
        """
        # Aggregate stats
        total_trades = len(self.history)
        wins = sum(1 for t in self.history if t.get("is_win", False))
        win_rate = round((wins / max(total_trades, 1)) * 100.0, 1)

        realized_usd = sum(t["net_pnl"] for t in self.history if t.get("currency") == "$")
        realized_inr = sum(t["net_pnl"] for t in self.history if t.get("currency") == "₹")

        unrealized_usd = sum(p["unrealized_pnl"] for p in self.positions.values() if p.get("currency") == "$")
        unrealized_inr = sum(p["unrealized_pnl"] for p in self.positions.values() if p.get("currency") == "₹")

        pos_rows = []
        for p in self.positions.values():
            cur = p["currency"]
            pos_rows.append({
                "Asset": p["ticker"],
                "Side": "🟢 BUY" if p["action"] == "BUY" else "🔴 SELL",
                "Shares": f"{p['quantity']:,}",
                "Entry Price": f"{cur}{p['entry_price']:,.2f}",
                "Current Price": f"{cur}{p['current_price']:,.2f}",
                "Stop Loss": f"{cur}{p['stop_loss']:,.2f}" if p.get("stop_loss") else "-",
                "Take Profit": f"{cur}{p['take_profit']:,.2f}" if p.get("take_profit") else "-",
                "Unrealized PnL": f"{cur}{p['unrealized_pnl']:+,.2f}",
                "Return %": f"{p['unrealized_pnl_pct']:+.2f}%",
                "Entry Time": p["entry_time"],
            })

        hist_rows = []
        for h in self.history[:15]:
            cur = h["currency"]
            hist_rows.append({
                "Asset": h["ticker"],
                "Side": h["action"],
                "Shares": f"{h['quantity']:,}",
                "Entry": f"{cur}{h['entry_price']:,.2f}",
                "Exit": f"{cur}{h['exit_price']:,.2f}",
                "Net PnL": f"{cur}{h['net_pnl']:+,.2f}",
                "Return %": f"{h['pnl_pct']:+.2f}%",
                "Exit Reason": h["reason"],
                "Exit Time": h["exit_time"],
            })

        return {
            "cash_usd": f"${self.cash_usd:,.2f}",
            "cash_inr": f"₹{self.cash_inr:,.2f}",
            "realized_usd": f"${realized_usd:+,.2f}",
            "realized_inr": f"₹{realized_inr:+,.2f}",
            "unrealized_usd": f"${unrealized_usd:+,.2f}",
            "unrealized_inr": f"₹{unrealized_inr:+,.2f}",
            "total_trades": total_trades,
            "win_rate_pct": f"{win_rate:.1f}%",
            "open_positions_count": len(self.positions),
            "positions_df": pd.DataFrame(pos_rows),
            "history_df": pd.DataFrame(hist_rows),
        }
