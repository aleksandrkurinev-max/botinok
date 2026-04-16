import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.enums import ParseMode

# ================= НАСТРОЙКИ =================
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ================= ВАШ ТОКЕН =================
# ⚠️ ВСТАВЬТЕ СЮДА ВАШ ТОКЕН ОТ <span style="color: hsl(var(--primary)); font-weight: 500;">@BotFather</span> ⚠️
BOT_TOKEN = "8339819988:AAE35waTsfbWJU7s9i92TCxyTq6HI-lH_g8"

# Пример правильного токена (не используйте этот):
# BOT_TOKEN = "1234567890:ABCdefGHIjklMNOpqrsTUVwxyz-123456789"

# ================= ПРОВЕРКА ТОКЕНА =================
if BOT_TOKEN == "ВАШ_ТОКЕН_ЗДЕСЬ":
    print("❌ ОШИБКА: Вы не вставили токен!")
    print("\n📱 Как получить токен:")
    print("1. Откройте Telegram")
    print("2. Найдите <span style="color: hsl(var(--primary)); font-weight: 500;">@BotFather</span>")
    print("3. Напишите /mybots")
    print("4. Выберите вашего бота")
    print("5. Нажмите 'API Token'")
    print("6. Скопируйте токен")
    print("\n💡 Вставьте токен в строку BOT_TOKEN = 'ваш_токен'")
    exit(1)

# ================= СОЗДАЕМ БОТА =================
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# ================= КОМАНДА /start =================
dp.message(Command("start"))
async def start_command(message: types.Message):
    user = message.from_user
    
    text = f"""
    👋 Привет, {user.first_name}!

    🤖 Я бот для обработки фото
    
    📸 Отправьте мне фото для обработки
    
    📝 Команды:
    /start - начать
    /help - помощь
    /test - тест
    
    Ваш ID: {user.id}
    """
    
    await message.answer(text, parse_mode=ParseMode.MARKDOWN)
    logger.info(f"Пользователь {user.id} начал работу")

# ================= КОМАНДА /help =================
dp.message(Command("help"))
async def help_command(message: types.Message):
    text = """
    📖 Помощь по боту
    
    Как отправить фото:
    1. Нажмите на скрепку
    2. Выберите "Фото"
    3. Отправьте изображение
    
    Команды:
    /start - начать работу
    /help - эта справка
    /test - тест соединения
    
    Требования к фото:
    • Формат: JPG, PNG
    • Размер: до 10 MB
    """
    
    await message.answer(text, parse_mode=ParseMode.MARKDOWN)

# ================= КОМАНДА /test =================
dp.message(Command("test"))
async def test_command(message: types.Message):
    try:
        bot_info = await bot.get_me()
        text = f"""
        ✅ Тест пройден!
        
        Бот: @{bot_info.username}
        Имя: {bot_info.first_name}
        
        Все системы работают
        """
        await message.answer(text, parse_mode=ParseMode.MARKDOWN)
    except Exception as e:
        await message.answer(f"❌ Ошибка: {e}")

# ================= ОБРАБОТКА ФОТО =================
dp.message(lambda message: message.photo is not None)
async def handle_photo(message: types.Message):
    await message.answer("📸 Получил фото! Обрабатываю...")
    await asyncio.sleep(1)
    await message.answer("✅ Фото обработано!")

# ================= ОБРАБОТКА ТЕКСТА =================
dp.message()
async def handle_text(message: types.Message):
    if message.text and not message.text.startswith('/'):
        await message.answer("Отправьте мне фото или используйте команды:\n/start\n/help\n/test")


# ================= ЗАПУСК =================
if __name__ == "__main__":
    asyncio.run(main())
