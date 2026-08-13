from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery

from config import ADMIN_ID
from database import add_source
from keyboards import admin_keyboard

router = Router()


# =========================
# پنل ادمین
# =========================

@router.message(Command("admin"))
async def admin_handler(message: Message):

    if message.from_user.id != ADMIN_ID:
        return

    await message.answer(
        "👑 پنل مدیریت Nextel\n\n"
        "یکی از گزینه‌های زیر را انتخاب کنید:",
        reply_markup=admin_keyboard()
    )


# =========================
# دکمه اضافه کردن سورس
# =========================

@router.callback_query(F.data == "admin_add_source")
async def admin_add_source_handler(callback: CallbackQuery):

    if callback.from_user.id != ADMIN_ID:
        await callback.answer(
            "❌ دسترسی ندارید.",
            show_alert=True
        )
        return

    await callback.message.answer(
        "➕ اضافه کردن سورس\n\n"
        "فرمت:\n"
        "/addsource نام | توضیحات | قیمت | FILE_ID\n\n"
        "مثال:\n"
        "/addsource ربات فروشگاهی | ربات حرفه‌ای | 50 سکه | FILE_ID"
    )

    await callback.answer()


# =========================
# دریافت اطلاعات سورس
# =========================

@router.message(Command("addsource"))
async def addsource_handler(message: Message):

    if message.from_user.id != ADMIN_ID:
        return

    data = message.text.replace(
        "/addsource",
        "",
        1
    ).strip()

    parts = [
        part.strip()
        for part in data.split("|")
    ]

    if len(parts) != 4:
        await message.answer(
            "❌ فرمت اشتباه است.\n\n"
            "/addsource نام | توضیحات | قیمت | FILE_ID"
        )
        return

    title = parts[0]
    description = parts[1]
    price = parts[2]
    file_id = parts[3]

    await add_source(
        title,
        description,
        price,
        file_id
    )

    await message.answer(
        f"✅ سورس با موفقیت اضافه شد!\n\n"
        f"📦 {title}\n"
        f"💰 قیمت: {price}\n\n"
        "🏆 به برترین سورس‌ها اضافه شد."
    )
