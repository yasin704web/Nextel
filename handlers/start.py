from aiogram import Router, F, Bot
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery

from config import REQUIRED_CHANNEL
from database import add_user
from keyboards import join_keyboard, main_keyboard


router = Router()


WELCOME_TEXT = """
سلام من Nextel هستم 🤖

من به شما سورس‌های برنامه‌نویسی، قالب سایت و خدمات دیگری می‌دهم.

ممنون که با من همراه شدید ❤️

لطفاً یکی از دکمه‌های زیر را فشار دهید.
"""


async def is_member(bot: Bot, user_id: int) -> bool:
    """
    بررسی می‌کند کاربر عضو کانال اجباری هست یا خیر.
    """

    try:

        member = await bot.get_chat_member(
            chat_id=REQUIRED_CHANNEL,
            user_id=user_id
        )

        return member.status in (
            "member",
            "administrator",
            "creator"
        )

    except Exception:

        return False


# =========================
# /start
# =========================

@router.message(CommandStart())
async def start_handler(
    message: Message,
    bot: Bot
):

    user = message.from_user

    # ذخیره کاربر در دیتابیس
    await add_user(
        user_id=user.id,
        username=user.username
    )

    # بررسی عضویت
    if not await is_member(bot, user.id):

        await message.answer(
            "👋 به Nextel خوش آمدید!\n\n"
            "برای استفاده از ربات ابتدا باید در کانال ما عضو شوید 👇",
            reply_markup=join_keyboard()
        )

        return

    # اگر قبلاً عضو بوده
    await message.answer(
        WELCOME_TEXT,
        reply_markup=main_keyboard()
    )


# =========================
# بررسی عضویت
# =========================

@router.callback_query(F.data == "check_join")
async def check_join_handler(
    callback: CallbackQuery,
    bot: Bot
):

    user_id = callback.from_user.id

    # بررسی دوباره عضویت
    if not await is_member(bot, user_id):

        await callback.answer(
            "❌ هنوز عضو کانال نشده‌اید.\n"
            "ابتدا عضو کانال شوید و دوباره روی "
            "«بررسی عضویت» بزنید.",
            show_alert=True
        )

        return

    # تأیید عضویت
    await callback.answer(
        "✅ عضویت شما تأیید شد!"
    )

    # نمایش معرفی Nextel
    await callback.message.edit_text(
        WELCOME_TEXT,
        reply_markup=main_keyboard()
    )
