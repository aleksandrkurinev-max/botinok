import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.enums import ParseMode

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Конфигурация
TOKEN = "8339819988:AAE35waTsfbWJU7s9i92TCxyTq6HI-lH_g8"

# Инициализация бота
bot = Bot(token=TOKEN)
dp = Dispatcher()

# Команда /start
dp.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer("✅ Бот работает! Отправьте /test для проверки.")

# Команда /test
dp.message(Command("test"))
async def cmd_test(message: Message):
    await message.answer("✅ Тест пройден! Бот отвечает.")

# Обработка текстовых сообщений
dp.message()
async def echo(message: Message):
    await message.answer(f"Вы написали: {message.text}")

# Запуск бота
async def main():
    print("🤖 Запускаю тестового бота...")
    try:
        # Проверяем подключение
        me = await bot.get_me()
        print(f"✅ Бот подключен: @{me.username}")
        
        await dp.start_polling(bot)
    except Exception as e:
        print(f"❌ Ошибка подключения: {e}")
        print("\nВозможные решения:")
        print("1. Проверьте интернет-соединение")
        print("2. Убедитесь, что токен правильный")
        print("3. Попробуйте использовать VPN")
        print("4. Проверьте настройки брандмауэра")

if __name__ == "__main__":
    asyncio.run(main())
