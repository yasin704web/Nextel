from aiogram import Router, F
from aiogram.types import CallbackQuery

from database import (
    get_sources,
    get_source,
    get_coins,
    remove_coins,
    add_purchase
)

from keyboards import (
    main_menu,
    buy_source,
    back_button
)


router = Router()


# =========================
# 🏆 برترین سورس‌ها
# =========================

@router.callback_query(F.data == "top_sources")
async def top_sources(callback: CallbackQuery):

    sources = await get_sources(is_vip=0)

    if not sources:

        await callback.message.edit_text(
            """
🏆 برترین سورس‌ها

❌ در حال حاضر هیچ سورسی در این بخش قرار نگرفته است.
""",
            reply_markup=back_button()
        )

        await callback.answer()
        return

    text = "🏆 برترین سورس‌های Nextel\n\n"

    for source in sources:

        source_id = source[0]
        title = source[1]
        description = source[2]
        price = source[3]

        text += (
            f"📦 {title}\n"
            f"📝 {description}\n"
            f"🪙 قیمت: {price} سکه\n\n"
        )

        text += f"➡️ برای مشاهده: `source:{source_id}`\n\n"

    await callback.message.edit_text(
        text,
        reply_markup=back_button()
    )

    await callback.answer()


# =========================
# 👑 سورس VIP
# =========================

@router.callback_query(F.data == "vip_sources")
async def vip_sources(callback: CallbackQuery):

    sources = await get_sources(is_vip=1)

    if not sources:

        await callback.message.edit_text(
            """
👑 سورس‌های VIP

❌ در حال حاضر هیچ سورس VIP موجود نیست.
""",
            reply_markup=back_button()
        )

        await callback.answer()
        return

    text = "👑 سورس‌های VIP\n\n"

    for source in sources:

        source_id = source[0]
        title = source[1]
        description = source[2]
        price = source[3]

        text += (
            f"👑 {title}\n"
            f"📝 {description}\n"
            f"🪙 قیمت: {price} سکه\n\n"
        )

        text += f"➡️ برای مشاهده: `source:{source_id}`\n\n"

    await callback.message.edit_text(
        text,
        reply_markup=back_button()
    )

    await callback.answer()


# =========================
# 📦 مشاهده یک سورس
# =========================

@router.callback_query(
    F.data.startswith("source:")
)
async def show_source(callback: CallbackQuery):

    try:

        source_id = int(
            callback.data.split(":")[1]
        )

    except (IndexError, ValueError):

        await callback.answer(
            "❌ سورس نامعتبر است.",
            show_alert=True
        )

        return

    source = await get_source(source_id)

    if source is None:

        await callback.answer(
            "❌ این سورس وجود ندارد.",
            show_alert=True
        )

        return

    title = source[1]
    description = source[2]
    price = source[3]
    is_vip = source[5]

    category = "👑 VIP" if is_vip else "🏆 برترین سورس"

    text = f"""
{category}

📦 {title}

📝 توضیحات:
{description}

🪙 قیمت:
{price} سکه
"""

    await callback.message.edit_text(
        text,
        reply_markup=buy_source(source_id)
    )

    await callback.answer()


# =========================
# 🛒 خرید سورس
# =========================

@router.callback_query(
    F.data.startswith("buy_source:")
)
async def buy_source_handler(callback: CallbackQuery):

    try:

        source_id = int(
            callback.data.split(":")[1]
        )

    except (IndexError, ValueError):

        await callback.answer(
            "❌ سورس نامعتبر است.",
            show_alert=True
        )

        return

    user_id = callback.from_user.id

    source = await get_source(source_id)

    if source is None:

        await callback.answer(
            "❌ این سورس دیگر موجود نیست.",
            show_alert=True
        )

        return

    title = source[1]
    price = source[3]
    file_id = source[4]

    coins = await get_coins(user_id)

    # =========================
    # ❌ سکه کافی نیست
    # =========================

    if coins < price:

        missing = price - coins

        text = f"""
❌ سکه کافی نیست!

📦 سورس:
{title}

🪙 قیمت:
{price} سکه

💰 موجودی شما:
{coins} سکه

📉 سکه موردنیاز:
{missing} سکه دیگر

🎡 می‌توانید شانس خود را در گردونه امتحان کنید.
"""

        await callback.message.edit_text(
            text,
            reply_markup=back_button()
        )

        await callback.answer()

        return

    # =========================
    # 💳 کسر سکه
    # =========================

    success = await remove_coins(
        user_id,
        price
    )

    if not success:

        await callback.answer(
            "❌ خرید انجام نشد. موجودی سکه شما تغییر کرده است.",
            show_alert=True
        )

        return

    # =========================
    # ثبت خرید
    # =========================

    await add_purchase(
        user_id,
        source_id,
        price
    )

    # =========================
    # ارسال فایل
    # =========================

    try:

        await callback.message.answer_document(
            document=file_id,
            caption=f"""
✅ خرید با موفقیت انجام شد!

📦 {title}

🪙 هزینه:
{price} سکه

💰 موجودی باقی‌مانده:
{coins - price} سکه

❤️ ممنون از خرید شما از Nextel
"""
        )

        await callback.answer(
            "✅ خرید موفق بود!"
        )

    except Exception:

        # اگر ارسال فایل با مشکل مواجه شد،
        # مبلغ را برگردانیم.

        from database import add_coin

        await add_coin(
            user_id,
            price
        )

        await callback.answer(
            "❌ ارسال فایل با مشکل مواجه شد و سکه‌ها برگشت داده شدند.",
            show_alert=True
        )
