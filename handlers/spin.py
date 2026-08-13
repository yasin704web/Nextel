from aiogram import Router, F
from aiogram.types import CallbackQuery

from datetime import date
import random

from database import (
    get_coins,
    add_coin,
    get_last_spin,
    update_last_spin
)

from keyboards import back_keyboard


router = Router()


@router.callback_query(F.data == "spin")
async def spin_handler(callback: CallbackQuery):

    user_id = callback.from_user.id

    today = date.today().isoformat()

    # بررسی اینکه کاربر امروز قبلاً گردونه زده یا نه
    last_spin = await get_last_spin(user_id)

    if last_spin == today:

        await callback.answer(
            "⏳ امروز قبلاً گردونه را امتحان کرده‌ای!\n"
            "فردا دوباره شانست را امتحان کن 🏆",
            show_alert=True
        )

        return

    # ثبت استفاده امروز
    await update_last_spin(
        user_id,
        today
    )

    # احتمال برد
    # 20 درصد برنده
    won = random.random() < 0.20

    if won:

        # اضافه کردن یک سکه
        await add_coin(user_id)

        coins = await get_coins(user_id)

        text = f"""
🎉 تبریک قهرمان!

🪙 امروز یک سکه گرفتید!

━━━━━━━━━━━━━━━━━━

💰 موجودی فعلی شما:
{coins} 🪙

با سکه‌ها می‌توانید سورس‌های VIP تهیه کنید. 👑

🚀 موفق باشید!
"""

    else:

        text = """
😅 این بار شانسی در نظر گرفته نشد!

ولی تلاش کن قهرمان 🏆

⏳ فردا دوباره می‌تونی شانس خودت رو امتحان کنی.
"""

    await callback.message.edit_text(
        text,
        reply_markup=back_keyboard()
    )

    await callback.answer()
