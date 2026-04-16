import asyncio
import logging
from pathlib import Path
from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.enums import ParseMode

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Конфигурация
TOKEN = "8339819988:AAE35waTsfbWJU7s9i92TCxyTq6HI-lH_g8"
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB

# Создаем папку для временных файлов
TEMP_DIR = Path("temp_files")
TEMP_DIR.mkdir(exist_ok=True)

# Инициализация бота
bot = Bot(token=TOKEN)
dp = Dispatcher()

# Команда /start
dp.message(Command("start"))
async def cmd_start(message: Message):
    welcome_text = """
    👋 *Добро пожаловать в Photo Animator Bot!*
    
    Я могу оживить ваши фотографии! 📸✨
    
    *Как использовать:*
    1. Отправьте мне фотографию
    2. Я обработаю её
    3. Получите анимированный результат!
    
    *Поддерживаемые форматы:*
    • JPG, JPEG, PNG, WebP
    
    *Ограничения:*
    • Максимальный размер: 10 MB
    
    *Команды:*
    /start - Начать работу
    /help - Помощь
    /status - Статус бота
    
    Отправьте фото, чтобы начать!
    """
    await message.answer(welcome_text, parse_mode=ParseMode.MARKDOWN)

# Команда /help
dp.message(Command("help"))
async def cmd_help(message: Message):
    help_text = """
    *📖 Помощь по использованию бота*
    
    *Как отправить фото:*
    1. Нажмите на скрепку (📎)
    2. Выберите "Фото" или "Галерея"
    3. Выберите фотографию
    4. Отправьте
    
    *Что происходит:*
    1. Я проверяю фото
    2. Сохраняю для обработки
    3. Отправляю на сервер
    4. Возвращаю результат
    
    *Техническая поддержка:*
    Если возникли проблемы, опишите их подробно.
    """
    await message.answer(help_text, parse_mode=ParseMode.MARKDOWN)

# Команда /status
dp.message(Command("status"))
async def cmd_status(message: Message):
    status_text = """
    *📊 Статус бота*
    
    ✅ Бот активен и работает
    📈 Готов к обработке фото
    ⏱️ Среднее время обработки: 30-60 сек
    
    *Статистика:*
    • Фото обработано: 0 (пока нет данных)
    • Доступность: 100%
    
    Бот работает в тестовом режиме.
    """
    await message.answer(status_text, parse_mode=ParseMode.MARKDOWN)

# Обработка фото
dp.message(F.photo)
async def handle_photo(message: Message):
    try:
        user = message.from_user
        logger.info(f"Фото от пользователя {user.id} ({user.username})")
        
        # Отправляем сообщение о начале обработки
        processing_msg = await message.answer("📥 Получил ваше фото! Проверяю...")
        
        # Получаем фото (самое высокое качество)
        photo = message.photo[-1]
        file_info = await bot.get_file(photo.file_id)
        
        # Проверяем размер файла
        if photo.file_size > MAX_FILE_SIZE:
            await processing_msg.edit_text(
                "❌ *Фото слишком большое!*\n\n"
                f"Максимальный размер: {MAX_FILE_SIZE // (1024*1024)} MB\n"
                f"Ваш файл: {photo.file_size // (1024*1024)} MB\n\n"
                "Пожалуйста, уменьшите размер фото.",
                parse_mode=ParseMode.MARKDOWN
            )
            return
        
        await processing_msg.edit_text("✅ Фото прошло проверку! Сохраняю...")
        
        # Сохраняем фото
        temp_file = TEMP_DIR / f"photo_{user.id}_{message.message_id}.jpg"
        await bot.download_file(file_info.file_path, temp_file)
        
        await processing_msg.edit_text(
            "🔄 *Фото сохранено!*\n\n"
            "Сейчас функция оживления фото доступна по подписке.\n\n"
            "*Для доступа к полной функциональности:*\n"
            "1. Оформите подписку\n"
            "2. Получите API ключ\n"
            "3. Интегрируйте в код бота",
            parse_mode=ParseMode.MARKDOWN
        )
        
        # Информация о файле
        file_info_text = f"""
        *Информация о файле:*
        • Размер: {temp_file.stat().st_size // 1024} KB
        • Путь: `{temp_file}`
        • Временный файл будет удален
        """
        
        await message.answer(file_info_text, parse_mode=ParseMode.MARKDOWN)
        
    except Exception as e:
        logger.error(f"Ошибка при обработке фото: {e}")
        await message.answer(
            "❌ *Произошла ошибка!*\n\n"
            "Пожалуйста, попробуйте еще раз.",
            parse_mode=ParseMode.MARKDOWN
        )

# Обработка документов (фото как файл)
dp.message(F.document)
async def handle_document(message: Message):
    document = message.document
    
    # Проверяем, является ли документ изображением
    if document.mime_type and document.mime_type.startswith('image/'):
        await handle_photo(message)
    else:
        await message.answer(
            "❌ *Это не изображение!*\n\n"
            "Пожалуйста, отправьте фото в формате JPG, PNG или JPEG.",
            parse_mode=ParseMode.MARKDOWN
        )

# Запуск бота
async def main():
    print("🤖 Бот запускается...")
    print(f"📁 Временная папка: {TEMP_DIR.absolute()}")
    print("⚡ Используйте Ctrl+C для остановки")
    
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
