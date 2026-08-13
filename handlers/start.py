from aiogram import Router, F
from aiogram.types import Message, CallbackQuery

from keyboards import join_keyboard, main_keyboard
from database import add_user


router = Router()


# =========================
# بررسی عضویت
# =========================

async def check_membership(bot, user_id):

    channels = [
        "@SaaSbot_io",
        "@likethedeath"
    ]

    for channel in channels:

        try:

            member = await bot.get_chat_member(
                chat_id=channel,
                user_id=user_id
            )

            if member.status in [
                "left",
                "kicked"
            ]:

                return False

        except Exception:

            return False

    return True


# =========================
# /start
# =========================

@router.message(F.text == "/start")
async def start_handler(message: Message):

    await add_user(
        user_id=message.from_user.id,
        username=message.from_user.username,
        full_name=message.from_user.full_name
    )

    await message.answer(
        """
🤖 برای استفاده از Nextel ابتدا در کانال‌های زیر عضو شوید:

📢 کانال 1
👤 کانال 2

بعد از عضویت روی «✅ تأیید عضویت» بزنید.
""",
        reply_markup=join_keyboard()
    )


# =========================
# تأیید عضویت
# =========================

@router.callback_query(F.data == "check_membership")
async def check_membership_handler(
    callback: CallbackQuery
):

    is_member = await check_membership(
        callback.bot,
        callback.from_user.id
    )

    if not is_member:

        await callback.answer(
            "❌ هنوز در کانال‌ها عضو نشده‌اید.",
            show_alert=True
        )

        return

    text = """
🤖 سلام! من Nextel هستم.

من به شما سورس‌های برنامه‌نویسی، قالب سایت و خدمات دیگری ارائه می‌دهم.

ممنون که با من همراه شدید ❤️

لطفاً یکی از دکمه‌های زیر را انتخاب کنید.
"""

    await callback.message.edit_text(
        text,
        reply_markup=main_keyboard()
    )

    await callback.answer(
        "✅ عضویت شما تأیید شد!"
    )
