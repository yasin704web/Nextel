import random
from datetime import date

from aiogram import Router, F
from aiogram.types import CallbackQuery

from database import (
    get_last_spin,
    update_last_spin,
    add_coin,
    get_coins
)

from keyboards import back_button


router = Router()


# =========================
# 🎡 گردونه شانس
# =========================

@router.callback_query(F.data == "spin")
async def spin_handler(callback: CallbackQuery):

    user_id = callback.from_user.id

    today = date.today().isoformat()

    # بررسی استفاده قبلی در امروز
    last_spin = await get_last_spin(user_id)

    if last_spin == today:

        coins = await get_coins(user_id)

        text = f"""
🎡 گردونه شانس Nextel

⚠️ شما امروز قبلاً از گردونه استفاده کرده‌اید.

🪙 موجودی فعلی شما:
{coins} سکه

⏳ فردا دوباره می‌توانید شانس خود را امتحان کنید.
"""

        await callback.message.edit_text(
            text,
            reply_markup=back_button()
        )

        await callback.answer()

        return

    # ثبت استفاده امروز
    await update_last_spin(
        user_id,
        today
    )

    # =========================
    # نتیجه گردونه
    # =========================

    # 30 درصد شانس دریافت سکه
    won = random.random() < 0.30

    if won:

        await add_coin(
            user_id,
            1
        )

        coins = await get_coins(user_id)

        text = f"""
🎉 تبریک قهرمان!

🎡 گردونه شانس

🪙 امروز یک سکه گرفتید!

✨ شانس با شما یار بود.

💰 موجودی فعلی:
{coins} سکه

🚀 از سکه‌هایتان برای تهیه سورس‌های Nextel استفاده کنید.
"""

    else:

        coins = await get_coins(user_id)

        text = f"""
🎡 گردونه شانس

😅 این بار شانسی در نظر گرفته نشد!

ولی ناامید نشو قهرمان 💪

🍀 فردا دوباره امتحان کن.

💰 موجودی فعلی:
{coins} سکه
"""

    await callback.message.edit_text(
        text,
        reply_markup=back_button()
    )

    await callback.answer()
