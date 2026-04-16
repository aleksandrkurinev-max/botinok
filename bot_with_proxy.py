import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.client.session.aiohttp import AiohttpSession
import aiohttp

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# ТОКЕН БОТА
TOKEN = "8622779229:AAHBdY80b2kTFTqhaC_AJBAyN182XYyXI-s"

# ================= НАСТРОЙКИ ПРОКСИ =================
# Вариант 1: SOCKS5 прокси (рекомендуется для Telegram)
# proxy_url = "socks5://username:password@proxy_ip:proxy_port"

# Вариант 2: HTTP прокси
# proxy_url = "http://username:password@proxy_ip:proxy_port"

# Вариант 3: БЕСПЛАТНЫЕ публичные прокси (осторожно, могут не работать)
# Примеры (замените на актуальные):
# proxy_url = "http://45.77.56.113:3128"  # HTTP прокси
# proxy_url = "socks5://138.197.157.32:1080"  # SOCKS5 прокси

# ================= СОЗДАЕМ СЕССИЮ =================
# Без прокси (попробуйте с VPN)
session = AiohttpSession()

# С прокси (раскомментируйте если нужно):
"""
session = AiohttpSession(
    connector=aiohttp.TCPConnector(
        ssl=False,
        proxy="http://ваш_прокси:порт"  # Замените на реальный прокси
    )
)
"""

# ================= СОЗДАЕМ БОТА =================
bot = Bot(token=TOKEN, session=session)
dp = Dispatcher()

# ================= КОМАНДЫ =================
dp.message(Command("start"))
async def start_handler(message: types.Message):
    await message.answer("🎉 Бот работает! Отправьте фото.")

dp.message(Command("help"))
async def help_handler(message: types.Message):
    await message.answer("Просто отправьте мне фото!")

# ================= ОБРАБОТКА ФОТО =================
dp.message(lambda m: m.photo is not None)
async def photo_handler(message: types.Message):
    await message.answer("📸 Получил фото! Обрабатываю...")
    await asyncio.sleep(2)
    await message.answer("✅ Фото обработано!\n\nФункция оживления фото доступна по подписке.")

# ================= ЗАПУСК =================
async def main():
    print("=" * 50)
    print("🤖 TELEGRAM BOT - ОЖИВЛЕНИЕ ФОТО")
    print("=" * 50)
    
    try:
        # Проверка подключения
        print("📡 Проверяю подключение к Telegram...")
        me = await bot.get_me()
        print(f"✅ Успешно! Бот: @{me.username}")
        print(f"👤 ID: {me.id}")
        print(f"📛 Имя: {me.first_name}")
        
        print("\n⚡ Бот запущен и готов к работе!")
        print("📱 Откройте Telegram -> найдите вашего бота")
        print("🔴 Нажмите Ctrl+C для остановки")
        print("=" * 50)
        
        # Запуск polling
        await dp.start_polling(bot)
        
    except Exception as e:
        print(f"\n❌ ОШИБКА ПОДКЛЮЧЕНИЯ: {e}")
        print("\n🔧 РЕШЕНИЕ:")
        print("1. ВКЛЮЧИТЕ VPN (ProtonVPN, Windscribe, Cloudflare WARP)")
        print("2. Запустите VPN приложение")
        print("3. Подключитесь к серверу")
        print("4. Запустите бота снова")
        print("\n📱 Бесплатные VPN:")
        print("• ProtonVPN: https://protonvpn.com")
        print("• Windscribe: https://windscribe.com")
        print("• Cloudflare WARP: https://1.1.1.1")

if __name__ == "__main__":
    asyncio.run(main())
