import asyncio

from aiogram import Bot, Dispatcher

from config import BOT_TOKEN
from database import init_db

from handlers_start import router as start_router
from handlers_menu import router as menu_router
from handlers_sources import router as sources_router
from handlers_admin import router as admin_router
from handlers_spin import router as spin_router


async def main():
    # ساخت ربات
    bot = Bot(token=BOT_TOKEN)

    # ساخت Dispatcher
    dp = Dispatcher()

    # ثبت Router ها
    dp.include_router(start_router)
    dp.include_router(menu_router)
    dp.include_router(sources_router)
    dp.include_router(admin_router)
    dp.include_router(spin_router)

    # راه‌اندازی دیتابیس
    await init_db()

    print("================================")
    print("🚀 Nextel Bot is running...")
    print("🤖 Bot started successfully")
    print("================================")

    # شروع دریافت پیام‌ها
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
