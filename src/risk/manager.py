"""Risk Management - Position Sizing & Limits"""
from dataclasses import dataclass

@dataclass
class RiskConfig:
    max_position_pct: float = 0.02    # 2% per trade
    stop_loss_pct: float = 0.05       # 5% stop loss
    max_daily_drawdown: float = 0.10  # 10% daily max loss
    cooldown_trades: int = 3           # Pause after N consecutive losses

class RiskManager:
    def __init__(self, **kwargs):
        self.config = RiskConfig(**kwargs)
        self.daily_pnl = 0.0
        self.consecutive_losses = 0
        self.cooldown_active = False
    
    def approve(self, order) -> bool:
        if self.cooldown_active:
            return False
        if self.daily_pnl <= -self.config.max_daily_drawdown:
            return False
        return True
    
    def record_trade(self, pnl: float):
        self.daily_pnl += pnl
        if pnl < 0:
            self.consecutive_losses += 1
            if self.consecutive_losses >= self.config.cooldown_trades:
                self.cooldown_active = True
        else:
            self.consecutive_losses = 0
            self.cooldown_active = False
    
    def reset_daily(self):
        self.daily_pnl = 0.0
