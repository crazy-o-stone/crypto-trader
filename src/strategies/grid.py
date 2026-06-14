"""Grid Trading Strategy"""
from dataclasses import dataclass
from typing import Optional

@dataclass
class Order:
    side: str       # "buy" or "sell"
    size: float
    price: float
    symbol: str = "WETH/USDC"

class GridStrategy:
    def __init__(self, grid_size: int = 10, spacing: float = 0.01):
        self.grid_size = grid_size
        self.spacing = spacing
        self.grid_levels = []
        self.interval = 5  # seconds between ticks
    
    async def on_tick(self, price: float, position) -> Optional[Order]:
        self._update_grid(price)
        
        for level in self.grid_levels:
            if not level["filled"] and price <= level["price"] and level["side"] == "buy":
                level["filled"] = True
                return Order(side="buy", size=self._calc_size(price), price=level["price"])
            if level["filled"] and price >= level["price"] * (1 + self.spacing) and level["side"] == "sell":
                level["filled"] = False
                return Order(side="sell", size=self._calc_size(price), price=level["price"])
        return None
    
    def _update_grid(self, current_price: float):
        if not self.grid_levels:
            for i in range(-self.grid_size // 2, self.grid_size // 2 + 1):
                self.grid_levels.append({
                    "price": current_price * (1 + i * self.spacing),
                    "side": "buy" if i < 0 else "sell",
                    "filled": i >= 0,
                })
    
    def _calc_size(self, price: float) -> float:
        return 0.1  # Fixed size, risk manager adjusts
