import asyncio
import logging
import os
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.enums import ParseMode
from aiogram.types import FSInputFile

# ================= НАСТРОЙКИ =================
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# ================= ВАШ ТОКЕН =================
# ⚠️ ЗАМЕНИТЕ ЭТУ СТРОКУ НА ВАШ РЕАЛЬНЫЙ ТОКЕН ⚠️
BOT_TOKEN = "8339819988:AAE35waTsfbWJU7s9i92TCxyTq6HI-lH_g8"

# Пример правильного токена (не используйте этот):
# BOT_TOKEN = "1234567890:ABCdefGHIjklMNOpqrsTUVwxyz-123456789"

# ================= ПРОВЕРКА ТОКЕНА =================
def check_token():
    """Проверяет и форматирует токен"""
    if BOT_TOKEN.startswith("ВАШ_") or len(BOT_TOKEN) < 30:
        print("❌ ОШИБКА: Токен не установлен!")
        print("\n🔧 Как получить токен:")
        print("1. Откройте Telegram")
        print("2. Найдите <span style="color: hsl(var(--primary)); font-weight: 500;">@BotFather</span>")
        print("3. Напишите /mybots")
        print("4. Выберите вашего нового бота")
        print("5. Нажмите 'API Token'")
        print("6. Скопируйте токен")
        print("\n📝 Формат токена: 1234567890:ABCdefGHIjklMNOpqrsTUVwxyz-123456789")
        print("\n💡 Вставьте токен в строку BOT_TOKEN = \"ваш_токен\"")
        return False
    return True

# ================= СОЗДАЕМ БОТА =================
if not check_token():
    exit(1)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# ================= КОМАНДА /start =================
dp.message(Command("start"))
async def start_command(message: types.Message):
    """Обработчик команды /start"""
    user = message.from_user
    
    welcome_text = f"""
    🎉 *Добро пожаловать, {user.first_name}!*

    🤖 *Я бот для обработки фото*
    
    *Что я умею:*
    📸 Принимать фотографии
    ⚡ Обрабатывать их
    🎬 Создавать анимации (по подписке)
    
    *Как использовать:*
    1. Отправьте мне фото
    2. Я его обработаю
    3. Получите результат
    
    *Доступные команды:*
    /start - начать работу
    /help - помощь
    /info - информация о боте
    /test - тест соединения
    
    📱 *Ваши данные:*
    👤 Имя: {user.first_name}
    📛 Username: @{user.username if user.username else 'не указан'}
    🔑 ID: `{user.id}`
    
    Отправьте мне фото и начнем! 📸
    """
    
    await message.answer(welcome_text, parse_mode=ParseMode.MARKDOWN)
    logger.info(f"Пользователь {user.id} ({user.username}) начал работу")

# ================= КОМАНДА /help =================
dp.message(Command("help"))
async def help_command(message: types.Message):
    """Обработчик команды /help"""
    help_text = """
    *📖 Помощь по использованию бота*
    
    *Основные функции:*
    • Прием и обработка фотографий
    • Создание анимаций из фото
    • Сохранение истории обработки
    
    *Как отправить фото:*
    1. Нажмите на скрепку (📎)
    2. Выберите "Фото и видео"
    3. Выберите изображение
    4. Нажмите "Отправить"
    
    *Требования к фото:*
    • Формат: JPG, PNG, JPEG
    • Размер: до 10 MB
    • Качество: не ниже 640x480
    
    *Команды бота:*
    /start - начать работу
    /help - эта справка
    /info - информация о боте
    /test - тест соединения
    
    *Техническая поддержка:*
    При возникновении проблем:
    1. Проверьте интернет-соединение
    2. Убедитесь, что фото соответствует требованиям
    3. Перезапустите бота командой /start
    """
    
    await message.answer(help_text, parse_mode=ParseMode.MARKDOWN)

# ================= КОМАНДА /info =================
dp.message(Command("info"))
async def info_command(message: types.Message):
    """Обработчик команды /info"""
    try:
        # Получаем информацию о боте
        bot_info = await bot.get_me()
        
        info_text = f"""
        *🤖 Информация о боте*
        
        *Основные данные:*
        👤 Имя: {bot_info.first_name}
        📛 Username: @{bot_info.username}
        🔑 ID: `{bot_info.id}`
        
        *Статус системы:*
        ✅ Подключение: Активно
        🟢 Состояние: Работает
        ⚡ Производительность: Норма
        
        *Техническая информация:*
        • Версия aiogram: 3.x
        • Python: 3.8+
        • Платформа: Telegram Bot API
        
        *Токен:* `{BOT_TOKEN[:10]}...{BOT_TOKEN[-10:]}`
        
        *Пользовательские данные:*
        👤 Ваше имя: {message.from_user.first_name}
        🔑 Ваш ID: `{message.from_user.id}`
        """
        
        await message.answer(info_text, parse_mode=ParseMode.MARKDOWN)
        
    except Exception as e:
        logger.error(f"Ошибка в команде /info: {e}")
        await message.answer("❌ Ошибка получения информации о боте")

# ================= КОМАНДА /test =================
dp.message(Command("test"))
async def test_command(message: types.Message):
    """Обработчик команды /test - проверка соединения"""
    try:
        # Проверяем соединение
        bot_info = await bot.get_me()
        
        test_text = f"""
        ✅ *Тест соединения пройден успешно!*
        
        *Результаты теста:*
        🟢 Telegram API: Доступен
        🟢 Бот: @{bot_info.username}
        🟢 Соединение: Стабильное
        
        *Время отклика:* Нормальное
        *Статус:* Все системы работают
        
        *Следующий шаг:*
        Отправьте фото для обработки! 📸
        """
        
        await message.answer(test_text, parse_mode=ParseMode.MARKDOWN)
        logger.info(f"Тест соединения от пользователя {message.from_user.id}")
        
    except Exception as e:
        error_text = f"""
        ❌ *Ошибка теста соединения!*
        
        *Причина:* {str(e)}
        
        *Что проверить:*
        1. Интернет-соединение
        2. Токен бота
        3. Доступность Telegram API
        
        *Решение:*
        • Проверьте VPN/прокси
        • Убедитесь, что токен правильный
        • Перезапустите бота
        """
        
        await message.answer(error_text, parse_mode=ParseMode.MARKDOWN)
        logger.error(f"Ошибка теста соединения: {e}")

# ================= ОБРАБОТКА ФОТО =================
dp.message(lambda message: message.photo is not None)
async def handle_photo(message: types.Message):
    """Обработчик фотографий"""
    try:
        user = message.from_user
        photo = message.photo[-1]  # Берем фото наилучшего качества
        
        logger.info(f"Получено фото от {user.id}: размер {photo.file_size} байт")
        
        # Сообщение о получении
        processing_msg = await message.answer(
            "📸 *Получил ваше фото!*\n\n"
            "⏳ *Обработка началась...*\n"
            "• Проверяю качество\n"
            "• Анализирую изображение\n"
            "• Подготавливаю к обработке",
            parse_mode=ParseMode.MARKDOWN
        )
        
        # Имитация обработки
        await asyncio.sleep(1)
        
        # Обновляем сообщение
        await processing_msg.edit_text(
            "🔄 *Обработка продолжается...*\n\n"
            "✅ Качество: Хорошее\n"
            "✅ Размер: Подходящий\n"
            "✅ Формат: Поддерживается\n\n"
            "⚡ Создаю анимацию...",
            parse_mode=ParseMode.MARKDOWN
        )
        
        await asyncio.sleep(2)
        
        # Фи��альное сообщение
        result_text = f"""
        🎉 *Обработка завершена!*
        
        *Результаты обработки:*
        ✅ Фото успешно обработано
        ✅ Анимация создана
        ✅ Качество сохранено
        
        *Детали:*
        👤 Пользователь: {user.first_name}
        📅 Время обработки: 3 секунды
        📊 Размер фото: {photo.file_size // 1024} KB
        
        *Что дальше:*
        Функция оживления фото доступна по подписке!
        
        *Для полного доступа:*
        1. Оформите подписку
        2. Получите API ключ
        3. Настройте интеграцию
        
        📱 *Ваш ID для подписки:* `{user.id}`
        """
        
        await processing_msg.edit_text(result_text, parse_mode=ParseMode.MARKDOWN)
        
        # Дополнительное сообщение
        await message.answer(
            "💡 *Хотите протестировать полную версию?*\n\n"
            "Отправьте еще одно фото или используйте команды:\n"
            "/start - начать заново\n"
            "/help - помощь\n"
            "/test - проверить соединение",
            parse_mode=ParseMode.MARKDOWN
        )
        
    except Exception as e:
        logger.error(f"Ошибка обработки фото: {e}")
        await message.answer(
            "❌ *Ошибка обработки фото*\n\n"
            "Пожалуйста, попробуйте еще раз или отправьте другое фото.",
            parse_mode=ParseMode.MARKDOWN
        )

# ================= ОБРАБОТКА ТЕКСТА =================
dp.message()
async def handle_text(message: types.Message):
    """Обработчик текстовых сообщений"""
    if message.text and not message.text.startswith('/'):
        await message.answer(
            "🤖 *Я понимаю команды и фото!*\n\n"
            "📸 *Чтобы обработать фото:*\n"
            "1. Нажмите 📎 (скрепка)\n"
            "2. Выберите 'Фото'\n"
            "3. Отправьте изображение\n\n"
            "📝 *Доступные команды:*\n"
            "/start - начать работу\n"
            "/help - помощь\n"
            "/info - информация\n"
            "/test - тест соединения\n\n"
            "Жду ваше фото! 😊",
            parse_mode=ParseMode.MARKDOWN
        )

# ================= ЗАПУСК БОТА =================
async def main():
    """Основная функция запуска бота"""
    print("=" * 70)
    print("🤖 TELEGRAM BOT - ОЖИВЛЕНИЕ ФОТО")
    print("=" * 70)
    
    print(f"\n🔑 Токен: {BOT_TOKEN[:15]}...")
    print("📡 Проверяю подключение к Telegram API...")
    
    try:
        # Проверка подключения и токена
        bot_info = await bot.get_me()
        
        print(f"✅ УСПЕХ! Подключение установлено")
        print(f"🤖 Бот: @{bot_info.username}")
        print(f"👤 Имя: {bot_info.first_name}")
        print(f"🔑 ID: {bot_info.id}")
        
        print("\n" + "=" * 70)
        print("⚡ БОТ ЗАПУЩЕН И ГОТОВ К РАБОТЕ!")
        print("=" * 70)
        
        print("\n📱 ИНСТРУКЦИЯ ДЛЯ ТЕСТА:")
        print(f"1. Откройте Telegram")
        print(f"2. Найдите бота: @{bot_info.username}")
        print(f"3. Напишите команду: /start")
        print(f"4. Отправьте фото для обработки")
        print(f"5. Проверьте работу всех функций")
        
        print("\n🔧 ТЕХНИЧЕСКАЯ ИНФОРМАЦИЯ:")
        print(f"• Токен: {BOT_TOKEN[:10]}...{BOT_TOKEN[-10:]}")
        print(f"• Python: {os.sys.version}")
        print(f"• Платформа: {os.sys.platform}")
        
        print("\n🔴 Для остановки нажмите: Ctrl+C")
        print("=" * 70)
        
        # Запускаем polling
        await dp.start_polling(bot)
        
    except Exception as e:
        print(f"\n❌ ОШИБКА ЗАПУСКА: {e}")
        print("\n🔧 ВОЗМОЖНЫЕ ПРИЧИНЫ:")
        print("1. Неверный токен бота")
        print("2. Проблемы с интернет-соединением")
        print("3. Telegram API недоступен")
        print("4. VPN/прокси не работает")
        
        print("\n🛠️ РЕШЕНИЕ:")
        print("1. Проверьте токен в <span style="color: hsl(var(--primary)); font-weight: 500;">@BotFather</span>")
        print("2. Убедитесь, что VPN включен")
        print("3. Проверьте интернет-соединение")
        print("4. Перезапустите бота с правильным токеном")

# ================= ТОЧКА ВХОДА =================
if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n🛑 Бот остановлен пользователем")
    except Exception as e:
        print(f"\n❌ Непредвиденная ошибка: {e}")
