"""Crypto Trader - Automated DeFi Trading Bot"""
import asyncio
import logging
from dotenv import load_dotenv
from strategies.grid import GridStrategy
from strategies.dca import DCAStrategy
from exchanges.uniswap import UniswapExchange
from risk.manager import RiskManager
from notifications.telegram import TelegramNotifier

load_dotenv()

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

STRATEGIES = {
    "grid": GridStrategy,
    "dca": DCAStrategy,
}

async def main(strategy_name: str, network: str = "ethereum"):
    logger.info(f"Starting Crypto Trader | Strategy: {strategy_name} | Network: {network}")
    
    exchange = UniswapExchange(network=network)
    risk_mgr = RiskManager(
        max_position_pct=0.02,
        stop_loss_pct=0.05,
        max_daily_drawdown=0.10,
    )
    notifier = TelegramNotifier()
    
    strategy_cls = STRATEGIES.get(strategy_name)
    if not strategy_cls:
        logger.error(f"Unknown strategy: {strategy_name}")
        return
    
    strategy = strategy_cls()
    logger.info(f"Initialized {strategy.__class__.__name__}")
    
    await notifier.send(f"🤖 Crypto Trader started\nStrategy: {strategy_name}\nNetwork: {network}")
    
    try:
        while True:
            price = await exchange.get_price("WETH/USDC")
            position = await exchange.get_position()
            
            order = await strategy.on_tick(price, position)
            if order:
                if risk_mgr.approve(order):
                    tx = await exchange.execute(order)
                    await notifier.send(f"📊 Trade: {order.side} {order.size} @ {price}\nTX: {tx}")
                else:
                    logger.warning(f"Risk manager rejected order: {order}")
            
            await asyncio.sleep(strategy.interval)
    except KeyboardInterrupt:
        logger.info("Shutting down...")
        await notifier.send("🛑 Crypto Trader stopped")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--strategy", default="grid", help="Strategy: grid, dca")
    parser.add_argument("--network", default="ethereum", help="Network: ethereum, bsc, solana")
    args = parser.parse_args()
    asyncio.run(main(args.strategy, args.network))
