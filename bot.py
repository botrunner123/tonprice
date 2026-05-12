import asyncio
import requests
from telegram import Bot
import logging
import os
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TONPriceBot:
    def __init__(self, bot_token: str, channel_id: str):
        self.bot = Bot(token=bot_token)
        self.channel_id = channel_id
        
    def get_ton_price(self):

        try:
            url = "https://api.binance.com/api/v3/ticker/bookTicker"
    
            r = requests.get(
                url,
                params={"symbol": "TONUSDT"},
                timeout=5
            )
    
            logger.info(r.text)
    
            data = r.json()
    
            price = float(data["bidPrice"])
    
            return price
    
        except Exception as e:
            logger.error(f"Binance error: {e}")
    
        try:
            url = "https://api.coingecko.com/api/v3/simple/price"
    
            r = requests.get(
                url,
                params={
                    "ids": "the-open-network",
                    "vs_currencies": "usd"
                },
                timeout=5
            )
    
            data = r.json()
    
            if "the-open-network" in data:
                return data["the-open-network"]["usd"]
    
        except Exception as e:
            logger.error(f"CoinGecko error: {e}")
    
        return None
            
    
    async def start_bot(self):
        while True:
            try:
                await self.send_price_update()
                await asyncio.sleep(10)
            except Exception as e:
                logger.error(f"Error: {e}")
                await asyncio.sleep(5)

def main():
    # YOUR CONFIGURATION HERE
    BOT_TOKEN = os.environ.get("BOT_TOKEN")
    CHANNEL_ID = os.environ.get("CHANNEL_ID")
    
    bot = TONPriceBot(BOT_TOKEN, CHANNEL_ID)
    
    print("TON Price Bot Running")
    print(f"Channel: {CHANNEL_ID}")
    print("Updates every 30 seconds\n")
    
    asyncio.run(bot.start_bot())

if __name__ == "__main__":
    main()
