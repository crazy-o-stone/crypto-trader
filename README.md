# 🤖 Crypto Trader

Automated cryptocurrency trading bot with DEX support, custom strategy engine, risk management, and Telegram notifications. Built for DeFi on Ethereum, BSC, and Solana.

## Features

- **Multi-Exchange** — Uniswap V2/V3, PancakeSwap, Jupiter (Solana)
- **Strategy Engine** — Write custom strategies with a simple API
- **Risk Management** — Stop-loss, take-profit, max drawdown, position sizing
- **MEV Protection** — Private mempool routing, slippage control
- **Real-time Notifications** — Telegram/Discord alerts for trades, P&L, errors
- **Backtesting** — Test strategies against historical data before live trading
- **Dashboard** — Web UI to monitor positions and P&L

## Quick Start

```bash
pip install -r requirements.txt
cp config/example.env config/.env
# Edit .env with your keys
python src/main.py --strategy grid --network ethereum
```

## Architecture

```
src/
├── main.py              # Entry point
├── strategies/          # Trading strategies
│   ├── grid.py          # Grid trading
│   ├── dca.py           # Dollar-cost averaging  
│   ├── mean_revert.py   # Mean reversion
│   └── arbitrage.py     # Cross-DEX arbitrage
├── exchanges/           # Exchange connectors
│   ├── uniswap.py       # Uniswap V2/V3
│   ├── pancake.py       # PancakeSwap
│   └── jupiter.py       # Jupiter (Solana)
├── risk/                # Risk management
│   ├── manager.py       # Position sizing & limits
│   └── stop_loss.py     # Stop-loss/take-profit
└── notifications/       # Alert system
    ├── telegram.py      # Telegram bot
    └── discord.py       # Discord webhook
```

## Strategy Example

```python
from strategies.base import Strategy

class GridStrategy(Strategy):
    def __init__(self, grid_size=10, spacing=0.01):
        self.grid_size = grid_size
        self.spacing = spacing
    
    async def on_tick(self, price, position):
        if self.should_buy(price, position):
            return self.create_order(side="buy", size=self.calc_size(price))
        if self.should_sell(price, position):
            return self.create_order(side="sell", size=position.size)
```

## Risk Management

- Max 2% portfolio per trade
- Hard stop-loss at -5%
- Daily max drawdown: -10%
- Cooldown after consecutive losses

## License

MIT
