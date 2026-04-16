import logging
import os
import tempfile
from pathlib import Path
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Конфигурация
TOKEN = "8622779229:AAHBdY80b2kTFTqhaC_AJBAyN182XYyXI-s"  # Замените на ваш новый токен
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB
SUPPORTED_FORMATS = ['.jpg', '.jpeg', '.png', '.webp']

# Создаем папку для временных файлов
TEMP_DIR = Path("temp_files")
TEMP_DIR.mkdir(exist_ok=True)

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
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
    • Рекомендуемое разрешение: до 2000x2000px
    
    *Команды:*
    /start - Начать работу
    /help - Помощь и инструкции
    /status - Статус бота
    
    Отправьте фото, чтобы начать!
    """
    await update.message.reply_text(welcome_text, parse_mode='Markdown')

# Команда /help
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = """
    *📖 Помощь по использованию бота*
    
    *Как отправить фото:*
    1. Нажмите на скрепку (📎) в поле ввода
    2. Выберите "Фото" или "Галерея"
    3. Выберите фотографию
    4. Отправьте
    
    *Что происходит после отправки:*
    1. Я проверяю формат и размер фото
    2. Сохраняю фото для обработки
    3. Отправляю на сервер оживления
    4. Возвращаю вам результат
    
    *Возможные проблемы:*
    • Фото слишком большое → уменьшите размер
    • Неподдерживаемый формат → конвертируйте в JPG/PNG
    • Долгая обработка → подождите немного
    
    *Техническая поддержка:*
    Если возникли проблемы, опишите их подробно.
    """
    await update.message.reply_text(help_text, parse_mode='Markdown')

# Команда /status
async def status_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    status_text = """
    *📊 Статус бота*
    
    ✅ Бот активен и работает
    📈 Готов к обработке фото
    ⏱️ Среднее время обработки: 30-60 сек
    💾 Временные файлы: очищаются автоматически
    
    *Статистика:*
    • Фото обработано: 0 (пока нет данных)
    • Среднее время: не определено
    • Доступность: 100%
    
    Бот работает в тестовом режиме.
    Функция оживления фото доступна по подписке.
    """
    await update.message.reply_text(status_text, parse_mode='Markdown')

# Обработка фото
async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        user = update.message.from_user
        logger.info(f"Фото от пользователя {user.id} ({user.username})")
        
        # Отправляем сообщение о начале обработки
        processing_msg = await update.message.reply_text(
            "📥 Получил ваше фото! Проверяю...",
            parse_mode='Markdown'
        )
        
        # Получаем фото (самое высокое качество)
        photo_file = await update.message.photo[-1].get_file()
        
        # Проверяем размер файла
        if photo_file.file_size > MAX_FILE_SIZE:
            await processing_msg.edit_text(
                "❌ *Фото слишком большое!*\n\n"
                f"Максимальный размер: {MAX_FILE_SIZE // (1024*1024)} MB\n"
                f"Ваш файл: {photo_file.file_size // (1024*1024)} MB\n\n"
                "Пожалуйста, уменьшите размер фото и попробуйте снова."
            )
            return
        
        await processing_msg.edit_text("✅ Фото прошло проверку! Сохраняю...")
        
        # Сохраняем фото во временный файл
        temp_file = TEMP_DIR / f"photo_{user.id}_{update.message.message_id}.jpg"
        await photo_file.download_to_drive(temp_file)
        
        await processing_msg.edit_text(
            "🔄 *Фото сохранено!*\n\n"
            "Сейчас функция оживления фото доступна по подписке.\n\n"
            "*Для доступа к полной функциональности:*\n"
            "1. Оформите подписку\n"
            "2. Получите API ключ\n"
            "3. Интегрируйте в код бота\n\n"
            "А пока я могу только сохранять фото для тестирования."
        )
        
        # Здесь будет вызов API оживления фото после подписки
        # Пример структуры:
        # animated_video = await animate_photo_api(temp_file)
        # await update.message.reply_video(animated_video, caption="Ваше оживленное фото! ✨")
        
        # Информация о файле
        file_info = f"""
        *Информация о файле:*
        • Размер: {temp_file.stat().st_size // 1024} KB
        • Путь: `{temp_file}`
        • Временный файл будет удален
        """
        
        await update.message.reply_text(file_info, parse_mode='Markdown')
        
    except Exception as e:
        logger.error(f"Ошибка при обработке фото: {e}")
        await update.message.reply_text(
            "❌ *Произошла ошибка!*\n\n"
            "Пожалуйста, попробуйте еще раз или отправьте другое фото.\n"
            f"Ошибка: {str(e)}"
        )

# Обработка документов (фото как файл)
async def handle_document(update: Update, context: ContextTypes.DEFAULT_TYPE):
    document = update.message.document
    
    # Проверяем, является ли документ изображением
    if document.mime_type and document.mime_type.startswith('image/'):
        await handle_photo(update, context)
    else:
        await update.message.reply_text(
            "❌ *Это не изображение!*\n\n"
            "Пожалуйста, отправьте фото в формате JPG, PNG или JPEG."
        )

# Обработка ошибок
async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.error(f"Ошибка: {context.error}")
    
    if update and update.message:
        await update.message.reply_text(
            "⚠️ *Произошла непредвиденная ошибка!*\n\n"
            "Пожалуйста, попробуйте еще раз позже."
        )

# Очистка временных файлов
def cleanup_temp_files():
    """Очистка старых временных файлов"""
    try:
        for file in TEMP_DIR.glob("*"):
            if file.stat().st_mtime < (time.time() - 3600):  # Старше 1 часа
                file.unlink()
    except Exception as e:
        logger.error(f"Ошибка при очистке файлов: {e}")

# Основная функция
def main():
    # Проверяем токен
    if TOKEN == "ВАШ_НОВЫЙ_ТОКЕН_ЗДЕСЬ":
        print("❌ ОШИБКА: Замените TOKEN на ваш токен бота!")
        print("Получите новый токен в <span style="color: hsl(var(--primary)); font-weight: 500;">@BotFather</span> командой /newbot")
        return
    
    # Создаем приложение
    application = Application.builder().token(TOKEN).build()
    
    # Добавляем обработчики команд
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("status", status_command))
    
    # Добавляем обработчики сообщений
    application.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    application.add_handler(MessageHandler(filters.Document.IMAGE, handle_document))
    
    # Обработчик ошибок
    application.add_error_handler(error_handler)
    
    # Запускаем бота
    print("🤖 Бот запускается...")
    print(f"📁 Временная папка: {TEMP_DIR.absolute()}")
    print("⚡ Используйте Ctrl+C для остановки")
    
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    import time
    cleanup_temp_files()  # Очищаем старые файлы при запуске
    main()
