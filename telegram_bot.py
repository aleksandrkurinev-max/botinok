import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command

logging.basicConfig(level=logging.INFO)

TOKEN = "8339819988:AAGeVKmrVlx5ckXvDIFQc2DGwIr2_RnuhNc"

bot = Bot(token=TOKEN)
dp = Dispatcher()

# Самый простой обработчик ВСЕХ сообщений
dp.message()
async def handle_all(message: types.Message):
    print(f"Получено сообщение: {message.text}")
    await message.answer(f"Получил: {message.text}")

async def main():
    print("🚀 Запускаю супер-простой бот...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
