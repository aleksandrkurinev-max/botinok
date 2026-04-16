import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.enums import ParseMode

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# ТОКЕН БОТА - ЗАМЕНИТЕ ЭТО НА ВАШ ТОКЕН!
BOT_TOKEN = "8622779229:AAHBdY80b2kTFTqhaC_AJBAyN182XYyXI-s"

# Создаем объекты бота и диспетчера
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# ================= КОМАНДА /start =================
dp.message(Command("start"))
async def start_command(message: types.Message):
    text = """
    👋 *Привет! Я бот для оживления фото!*
    
    Отправьте мне фотографию, и я обработаю её.
    
    *Команды:*
    /start - начать
    /help - помощь
    /status - статус
    
    Жду ваше фото! 📸
    """
    await message.answer(text, parse_mode=ParseMode.MARKDOWN)

# ================= КОМАНДА /help =================
dp.message(Command("help"))
async def help_command(message: types.Message):
    text = """
    *📖 Помощь*
    
    Просто отправьте мне фото!
    Я его проверю и обработаю.
    
    *Форматы:* JPG, PNG
    *Размер:* до 10 MB
    """
    await message.answer(text, parse_mode=ParseMode.MARKDOWN)

# ================= КОМАНДА /status =================
dp.message(Command("status"))
async def status_command(message: types.Message):
    text = """
    *📊 Статус бота*
    
    ✅ Работает
    🟢 Готов к приему фото
    ⚡ Все системы в норме
    """
    await message.answer(text, parse_mode=ParseMode.MARKDOWN)

# ================= ОБРАБОТКА ФОТО =================
dp.message(lambda m: m.photo is not None)
async def photo_handler(message: types.Message):
    # Отправляем сообщение о получении
    msg = await message.answer("📸 Получил фото! Обрабатываю...")
    
    # Имитация обработки
    await asyncio.sleep(2)
    
    # Результат
    await msg.edit_text(
        "✅ Фото обработано!\n\n"
        "Функция оживления фото доступна по подписке.\n"
        "Оформите подписку для полного доступа."
    )

# ================= ОБРАБОТКА ТЕКСТА =================
dp.message()
async def text_handler(message: types.Message):
    if message.text and not message.text.startswith('/'):
        await message.answer("Отправьте мне фото! 📸")

# ================= ЗАПУСК БОТА =================
async def main():
    print("=" * 40)
    print("🤖 БОТ ЗАПУСКАЕТСЯ")
    print("=" * 40)
    
    if BOT_TOKEN == "ВАШ_ТОКЕН_ЗДЕСЬ":
        print("\n❌ ОШИБКА: Замените BOT_TOKEN на ваш токен!")
        print("Токен получается в <span style="color: hsl(var(--primary)); font-weight: 500;">@BotFather</span>")
        return
    
    print(f"\n✅ Токен: {BOT_TOKEN[:10]}...")
    print("📱 Откройте Telegram -> найдите бота")
    print("⚡ Напишите /start")
    print("🔴 Ctrl+C для остановки")
    print("\n" + "=" * 40)
    
    try:
        await dp.start_polling(bot)
    except KeyboardInterrupt:
        print("\n🛑 Бот остановлен")

if __name__ == "__main__":
    asyncio.run(main())
