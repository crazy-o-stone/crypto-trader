"""Dollar-Cost Averaging Strategy"""
from typing import Optional
from .grid import Order

class DCAStrategy:
    def __init__(self, buy_amount: float = 100.0, interval_hours: int = 4):
        self.buy_amount = buy_amount
        self.interval_hours = interval_hours
        self.interval = interval_hours * 3600
        self.last_buy = 0
        self.total_invested = 0.0
        self.total_tokens = 0.0
    
    async def on_tick(self, price: float, position) -> Optional[Order]:
        current_time = position.timestamp if hasattr(position, "timestamp") else 0
        if current_time - self.last_buy >= self.interval:
            self.last_buy = current_time
            size = self.buy_amount / price
            self.total_invested += self.buy_amount
            self.total_tokens += size
            return Order(side="buy", size=size, price=price)
        return None
