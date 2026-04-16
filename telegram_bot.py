import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command

# ТОКЕН
TOKEN = "8339819988:AAE35waTsfbWJU7s9i92TCxyTq6HI-lH_g8"

bot = Bot(token=TOKEN)
dp = Dispatcher()

dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer("✅ Бот работает!")

async def main():
    print("🤖 Запуск...")
    try:
        me = await bot.get_me()
        print(f"✅ Бот: @{me.username}")
        await dp.start_polling(bot)
    except Exception as e:
        print(f"❌ Ошибка: {e}")

if __name__ == "__main__":
    asyncio.run(main())
