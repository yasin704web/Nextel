from aiogram import Router, F
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton

from database import get_sources
from keyboards import back_keyboard


router = Router()


@router.callback_query(F.data == "top_sources")
async def top_sources_handler(callback: CallbackQuery):

    sources = await get_sources()

    if not sources:

        await callback.message.edit_text(
            "🏆 برترین سورس‌ها\n\n"
            "در حال حاضر هیچ سورسی در این بخش قرار نگرفته است.",
            reply_markup=back_keyboard()
        )

        await callback.answer()
        return

    text = "🏆 برترین سورس‌ها | Nextel\n\n"

    buttons = []

    for source in sources:

        source_id, title, description, price, file_id = source

        text += (
            f"📦 {title}\n"
            f"📝 {description}\n"
            f"💰 قیمت: {price}\n"
            "━━━━━━━━━━━━━━━━━━\n"
        )

        buttons.append([
            InlineKeyboardButton(
                text=f"📦 {title}",
                callback_data=f"source_{source_id}"
            )
        ])

    buttons.append([
        InlineKeyboardButton(
            text="🔙 بازگشت",
            callback_data="back_main"
        )
    ])

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=buttons
    )

    await callback.message.edit_text(
        text,
        reply_markup=keyboard
    )

    await callback.answer()


# =========================
# انتخاب یک سورس
# =========================

@router.callback_query(F.data.startswith("source_"))
async def source_details_handler(callback: CallbackQuery):

    source_id = int(
        callback.data.split("_")[1]
    )

    sources = await get_sources()

    selected_source = None

    for source in sources:

        if source[0] == source_id:
            selected_source = source
            break

    if selected_source is None:

        await callback.answer(
            "❌ این سورس پیدا نشد.",
            show_alert=True
        )

        return

    _, title, description, price, file_id = selected_source

    text = f"""
📦 {title}

━━━━━━━━━━━━━━━━━━

📝 توضیحات:

{description}

━━━━━━━━━━━━━━━━━━

💰 قیمت:
{price}

━━━━━━━━━━━━━━━━━━

🚀 Nextel
"""

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🛒 خرید سورس",
                    callback_data=f"buy_source_{source_id}"
                )
            ],
            [
                InlineKeyboardButton(
                    text="🔙 بازگشت به برترین سورس‌ها",
                    callback_data="top_sources"
                )
            ]
        ]
    )

    await callback.message.edit_text(
        text,
        reply_markup=keyboard
    )

    await callback.answer()
