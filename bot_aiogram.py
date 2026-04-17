import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.types import Message
from aiogram.filters import Command

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Настройка прокси (если нужно)
# session = AiohttpSession(proxy="http://proxyuser:proxypass@proxy.server:port")

# Без прокси
session = AiohttpSession()

# Токен бота
TOKEN = "8339819988:AAGeVKmrVlx5ckXvDIFQc2DGwIr2_RnuhNc"

# Создаем бота с сессией
bot = Bot(token=TOKEN, session=session)
dp = Dispatcher()

dp.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer("✅ Бот работает через прямое подключение!")

dp.message()
async def echo(message: Message):
    await message.answer(f"Эхо: {message.text}")

async def main():
    print("🤖 Запускаю бота с проверкой сети...")
    
    try:
        # Простая проверка сети
        import socket
        socket.create_connection(("api.telegram.org", 443), timeout=5)
        print("✅ Соединение с Telegram API возможно")
    except Exception as e:
        print(f"❌ Не могу подключиться к Telegram: {e}")
        print("\n🎯 Решения:")
        print("1. Включите VPN")
        print("2. Проверьте интернет-соединение")
        print("3. Попробуйте позже")
        return
    
    try:
        me = await bot.get_me()
        print(f"✅ Бот подключен: @{me.username}")
        print("⚡ Бот запущен!")
        
        await dp.start_polling(bot)
    except Exception as e:
        print(f"❌ Ошибка при запуске: {e}")

if __name__ == "__main__":
    asyncio.run(main())