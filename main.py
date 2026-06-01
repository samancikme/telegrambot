import asyncio
import logging
import os
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from dotenv import load_dotenv
from handlers import router
import database

load_dotenv()

API_TOKEN = os.getenv('BOT_TOKEN')
if not API_TOKEN:
    raise RuntimeError('BOT_TOKEN environment variable is not set')

async def main():
    logging.basicConfig(level=logging.INFO)
    database.init_db()
    
    bot = Bot(token=API_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher()
    
    dp.include_router(router)
    
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
