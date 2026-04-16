import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.enums import ParseMode
from aiogram.client.session.aiohttp import AiohttpSession
import aiohttp

# ================= НАСТРОЙКИ =================
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ТОКЕН БОТА
BOT_TOKEN = "8622779229:AAHBdY80b2kTFTqhaC_AJBAyN182XYyXI-s"

# ================= НАСТРОЙКИ ПРОКСИ =================
# Вариант 1: Без прокси (если VPN включен)
USE_PROXY = False  # Измените на True если нужен прокси

# Вариант 2: С прокси (раскомментируйте и настройте)
PROXY_URL = None
# Примеры прокси:
# PROXY_URL = "http://username:password@proxy_ip:proxy_port"  # HTTP прокси
# PROXY_URL = "socks5://username:password@proxy_ip:proxy_port"  # SOCKS5 прокси

# ================= СОЗДАЕМ СЕССИЮ =================
if USE_PROXY and PROXY_URL:
    # Создаем сессию с прокси
    session = AiohttpSession(
        connector=aiohttp.TCPConnector(
            ssl=False,
            proxy=PROXY_URL
        )
    )
    print(f"🔗 Используется прокси: {PROXY_URL}")
else:
    # Обычная сессия
    session = AiohttpSession()
    print("🔗 Прокси не используется")

# ================= СОЗДАЕМ БОТА =================
bot = Bot(token=BOT_TOKEN, session=session)
dp = Dispatcher()

# ================= КОМАНДА /start =================
dp.message(Command("start"))
async def start_handler(message: types.Message):
    text = """
    🤖 *Бот для обработки фото*
    
    Отправьте мне фотографию для обработки.
    
    *Команды:*
    /start - начать
    /help - помощь
    /status - статус
    /test - тест соединения
    
    📸 Жду ваше фото!
    """
    await message.answer(text, parse_mode=ParseMode.MARKDOWN)

# ================= КОМАНДА /test =================
dp.message(Command("test"))
async def test_handler(message: types.Message):
    """Тест соединения с Telegram"""
    try:
        # Проверяем соединение
        me = await bot.get_me()
        text = f"""
        ✅ *Тест соединения пройден!*
        
        *Информация о боте:*
        👤 Имя: {me.first_name}
        📛 Username: @{me.username}
        🔑 ID: {me.id}
        
        *Статус:* Работает нормально
        """
        await message.answer(text, parse_mode=ParseMode.MARKDOWN)
    except Exception as e:
        await message.answer(f"❌ *Ошибка соединения:* {e}", parse_mode=ParseMode.MARKDOWN)

# ================= КОМАНДА /status =================
dp.message(Command("status"))
async def status_handler(message: types.Message):
    text = """
    *📊 Статус системы*
    
    🔗 *Соединение:* Проверяется...
    ⚡ *Бот:* Запущен
    📡 *Сеть:* Ожидание подключения
    
    *Для проверки:* /test
    """
    await message.answer(text, parse_mode=ParseMode.MARKDOWN)

# ================= ОБРАБОТКА ФОТО =================
dp.message(lambda message: message.photo is not None)
async def photo_handler(message: types.Message):
    await message.answer("📸 Получил фото! Обрабатываю...")
    await asyncio.sleep(1)
    await message.answer("✅ Фото обработано!\n\nФункция оживления фото доступна по подписке.")

# ================= ЗАПУСК БОТА =================
async def main():
    print("=" * 60)
    print("🤖 TELEGRAM BOT - РЕШЕНИЕ ПРОБЛЕМ С СОЕДИНЕНИЕМ")
    print("=" * 60)
    
    print(f"\n🔑 Токен: {BOT_TOKEN[:15]}...")
    print(f"🔗 Прокси: {'Используется' if USE_PROXY and PROXY_URL else 'Не используется'}")
    
    print("\n📡 Проверяю подключение к Telegram API...")
    
    try:
        # Тест подключения
        me = await bot.get_me()
        print(f"✅ УСПЕХ! Бот: @{me.username}")
        print(f"👤 Имя: {me.first_name}")
        print(f"🔑 ID: {me.id}")
        
        print("\n⚡ Бот готов к работе!")
        print("📱 Откройте Telegram -> найдите вашего бота")
        print("⚡ Напишите /start или /test")
        print("🔴 Ctrl+C для остановки")
        print("\n" + "=" * 60)
        
        # Запуск polling
        await dp.start_polling(bot)
        
    except Exception as e:
        print(f"\n❌ ОШИБКА ПОДКЛЮЧЕНИЯ: {e}")
        print("\n🔧 РЕШЕНИЯ:")
        print("1. ВКЛЮЧИТЕ VPN (BotHost или другой)")
        print("2. Проверьте доступность Telegram:")
        print("   • Откройте https://api.telegram.org в браузере")
        print("3. Используйте прокси:")
        print("   • Измените USE_PROXY = True")
        print("   • Укажите PROXY_URL")
        print("\n📱 Бесплатные VPN для теста:")
        print("• Cloudflare WARP: https://1.1.1.1")
        print("• ProtonVPN: https://protonvpn.com")
        print("• Windscribe: https://windscribe.com")

# ================= ТОЧКА ВХОДА =================
if __name__ == "__main__":
    asyncio.run(main())
