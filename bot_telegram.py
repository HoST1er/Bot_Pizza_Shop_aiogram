import asyncio
import logging

from aiogram import Bot

from create_bot import dp, bot
from handlers import client, other, admin


async def on_startup_bot(bot:Bot):
    print('Бот вышел в онлайн')

# Подключаем router
dp.include_router(client.client_router)
dp.include_router(other.other_router)
async def main():
    # dp.include_router(router)
    dp.startup.register(on_startup_bot)

    #await bot.delete_webhook(drop_pending_updates=True)

    # Запускаем поллинг диспетчера
    # dp.run_polling() автоматически вызывает on_startup и on_shutdown
    await dp.start_polling(bot) # или await dp.run_polling(bot)

if __name__ == "__main__":
    logging.info("Starting bot...")
    asyncio.run(main())