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
            url = "https://api.bybit.com/v5/market/tickers"
    
            r = requests.get(
                url,
                params={
                    "category": "spot",
                    "symbol": "TONUSDT"
                },
                timeout=5
            )
    
            data = r.json()
    
            price = float(
                data["result"]["list"][0]["lastPrice"]
            )
    
            return price
    
        except Exception as e:
            logger.error(f"Bybit error: {e}")
    
        return None
            
    async def send_price_update(self):
        price = self.get_ton_price()
    
        if price is not None:
    
            formatted_price = str(int(price * 1000) / 1000)
    
            await self.bot.send_message(
                chat_id=self.channel_id,
                text=formatted_price
            )
    
            logger.info(f"TON: {formatted_price}")
    
        else:
            logger.error("Price fetch failed")
    
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
