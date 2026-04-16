import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.enums import ParseMode

# ================= НАСТРОЙКИ =================
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ВАШ ТОКЕН ОТ <span style="color: hsl(var(--primary)); font-weight: 500;">@BotFather</span>
BOT_TOKEN = "8622779229:AAHBdY80b2kTFTqhaC_AJBAyN182XYyXI-s"

# ================= СОЗДАЕМ БОТА =================
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# ================= КОМАНДА /start =================
dp.message(Command("start"))
async def start_handler(message: types.Message):
    text = """
    👋 *Привет! Я бот для оживления фото!*
    
    Отправьте мне фотографию, и я её обработаю.
    
    *Команды:*
    /start - начать работу
    /help - помощь
    /status - статус бота
    
    Жду ваше фото! 📸
    """
    await message.answer(text, parse_mode=ParseMode.MARKDOWN)

# ================= КОМАНДА /help =================
dp.message(Command("help"))
async def help_handler(message: types.Message):
    text = """
    *📖 Помощь по использованию бота*
    
    *Как отправить фото:*
    1. Нажмите на скрепку (📎)
    2. Выберите "Фото"
    3. Выберите изображение
    4. Отправьте
    
    *Что я делаю:*
    • Проверяю фото
    • Обрабатываю его
    • Возвращаю результат
    
    *Ограничения:*
    • Размер: до 10 MB
    • Форматы: JPG, PNG, JPEG
    """
    await message.answer(text, parse_mode=ParseMode.MARKDOWN)

# ================= КОМАНДА /status =================
dp.message(Command("status"))
async def status_handler(message: types.Message):
    text = """
    *📊 Статус бота*
    
    ✅ *Состояние:* Работает
    🟢 *Готовность:* 100%
    ⚡ *Производительность:* Норма
    
    Все системы функционируют штатно!
    """
    await message.answer(text, parse_mode=ParseMode.MARKDOWN)

# ================= ОБРАБОТКА ФОТО =================
dp.message(lambda message: message.photo is not None)
async def photo_handler(message: types.Message):
    try:
        # Информация о пользователе
        user = message.from_user
        logger.info(f"Фото от {user.username} (ID: {user.id})")
        
        # Сообщение о получении
        msg = await message.answer("📸 *Получил фото!*\n\nПроверяю...", 
                                  parse_mode=ParseMode.MARKDOWN)
        
        # Получаем фото
        photo = message.photo[-1]
        
        # Проверка размера (10 MB)
        if photo.file_size > 10 * 1024 * 1024:
            await msg.edit_text(
                "❌ *Фото слишком большое!*\n\n"
                "Максимальный размер: 10 MB\n"
                "Пожалуйста, уменьшите фото.",
                parse_mode=ParseMode.MARKDOWN
            )
            return
        
        # Имитация обработки
        await asyncio.sleep(1)
        await msg.edit_text("✅ *Фото проверено!*\n\nОбрабатываю...", 
                           parse_mode=ParseMode.MARKDOWN)
        
        await asyncio.sleep(1)
        
        # Финальное сообщение
        await msg.edit_text(
            "🎉 *Обработка завершена!*\n\n"
            "Сейчас функция оживления фото доступна по подписке.\n\n"
            "*Для полного доступа:*\n"
            "1. Оформите подписку\n"
            "2. Получите API ключ\n"
            "3. Добавьте в код бота",
            parse_mode=ParseMode.MARKDOWN
        )
        
    except Exception as e:
        logger.error(f"Ошибка: {e}")
        await message.answer("❌ Ошибка обработки. Попробуйте еще раз.")

# ================= ОБРАБОТКА ТЕКСТА =================
dp.message()
async def text_handler(message: types.Message):
    if message.text and not message.text.startswith('/'):
        await message.answer(
            "Отправьте мне фото для обработки! 📸\n"
            "Или используйте команды:\n"
            "/start - начать\n"
            "/help - помощь\n"
            "/status - статус"
        )

# ================= ЗАПУСК БОТА =================
async def main():
    print("=" * 50)
    print("🤖 TELEGRAM BOT - ОЖИВЛЕНИЕ ФОТО")
    print("=" * 50)
    
    # Проверка токена
    if BOT_TOKEN == "8622779229:AAHBdY80b2kTFTqhaC_AJBAyN182XYyXI-s":
        print(f"\n✅ Токен: {BOT_TOKEN[:15]}...")
    else:
        print("\n❌ ОШИБКА: Проверьте токен!")
        return
    
    print("📱 Откройте Telegram -> найдите вашего бота")
    print("⚡ Напишите /start")
    print("📸 Отправьте фото для теста")
    print("🔴 Нажмите Ctrl+C для остановки")
    print("\n" + "=" * 50)
    
    try:
        await dp.start_polling(bot)
    except KeyboardInterrupt:
        print("\n\n🛑 Бот остановлен")
    except Exception as e:
        print(f"\n❌ Ошибка запуска: {e}")

# ================= ТОЧКА ВХОДА =================
if __name__ == "__main__":
    asyncio.run(main())
