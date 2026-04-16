import asyncio
import logging
from aiogram import Bot, Dispatcher, Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.enums import ParseMode

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Токен (убедитесь, что он правильный!)
TOKEN = "8339819988:AAGeVKmrVlx5ckXvDIFQc2DGwIr2_RnuhNc"

# Создаем роутер
router = Router()

# Команда /start
dp.message(Command("start"))
async def cmd_start(message: Message):
    logger.info(f"Получен /start от {message.from_user.id}")
    await message.answer(
        "🎉 *Бот работает!*\n\n"
        "Отправьте любое сообщение, и я отвечу.",
        parse_mode=ParseMode.MARKDOWN
    )

# Команда /help
dp.message(Command("help"))
async def cmd_help(message: Message):
    await message.answer(
        "📖 *Помощь*\n\n"
        "Доступные команды:\n"
        "/start - Начать работу\n"
        "/help - Помощь\n"
        "/test - Тестовая команда",
        parse_mode=ParseMode.MARKDOWN
    )

# Команда /test
dp.message(Command("test"))
async def cmd_test(message: Message):
    await message.answer("✅ Тест пройден! Бот отвечает.")

# Обработка ВСЕХ текстовых сообщений
dp.message()
async def echo_all(message: Message):
    logger.info(f"Сообщение от {message.from_user.id}: {message.text}")
    await message.answer(f"Вы написали: {message.text}")

async def main():
    # Инициализация
    bot = Bot(token=TOKEN)
    dp = Dispatcher()
    
    # Подключаем роутер
    dp.include_router(router)
    
    print("🤖 Запускаю бота...")
    
    try:
        # Проверка подключения
        me = await bot.get_me()
        print(f"✅ Бот: @{me.username}")
        print(f"✅ Имя: {me.first_name}")
        print(f"✅ ID: {me.id}")
        print("\n⚡ Бот готов к работе!")
        print("Отправьте /start в Telegram")
        
        # Запускаем опрос
        await dp.start_polling(bot)
        
    except Exception as e:
        print(f"❌ Ошибка: {e}")

if __name__ == "__main__":
    asyncio.run(main())
