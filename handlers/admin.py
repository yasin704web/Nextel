from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from config import ADMIN_ID

from database import (
    add_source,
    get_sources,
    delete_source,
    get_coins,
    get_user
)

from keyboards import admin_menu, admin_cancel


router = Router()


# =========================
# وضعیت افزودن سورس
# =========================

class AddSourceStates(StatesGroup):

    title = State()
    description = State()
    price = State()
    file = State()


# =========================
# بررسی ادمین
# =========================

def is_admin(user_id):

    return user_id == ADMIN_ID


# =========================
# /admin
# =========================

@router.message(F.text == "/admin")
async def admin_command(message: Message):

    if not is_admin(message.from_user.id):

        await message.answer(
            "⛔ شما دسترسی به پنل مدیریت ندارید."
        )

        return

    await message.answer(
        """
👑 پنل مدیریت Nextel

به پنل مدیریت خوش آمدید.
یکی از گزینه‌های زیر را انتخاب کنید:
""",
        reply_markup=admin_menu()
    )


# =========================
# ➕ افزودن سورس عادی
# =========================

@router.callback_query(F.data == "admin_add_source")
async def add_normal_source(
    callback: CallbackQuery,
    state: FSMContext
):

    if not is_admin(callback.from_user.id):

        await callback.answer(
            "⛔ دسترسی ندارید.",
            show_alert=True
        )

        return

    await state.update_data(is_vip=0)

    await state.set_state(
        AddSourceStates.title
    )

    await callback.message.edit_text(
        """
➕ افزودن سورس جدید

📦 مرحله 1 از 4

نام سورس را ارسال کنید:
""",
        reply_markup=admin_cancel()
    )

    await callback.answer()


# =========================
# 👑 افزودن سورس VIP
# =========================

@router.callback_query(F.data == "admin_add_vip")
async def add_vip_source(
    callback: CallbackQuery,
    state: FSMContext
):

    if not is_admin(callback.from_user.id):

        await callback.answer(
            "⛔ دسترسی ندارید.",
            show_alert=True
        )

        return

    await state.update_data(is_vip=1)

    await state.set_state(
        AddSourceStates.title
    )

    await callback.message.edit_text(
        """
👑 افزودن سورس VIP

📦 مرحله 1 از 4

نام سورس VIP را ارسال کنید:
""",
        reply_markup=admin_cancel()
    )

    await callback.answer()


# =========================
# مرحله 1: نام
# =========================

@router.message(AddSourceStates.title)
async def source_title(
    message: Message,
    state: FSMContext
):

    if not is_admin(message.from_user.id):

        return

    title = message.text.strip()

    if not title:

        await message.answer(
            "❌ نام سورس نمی‌تواند خالی باشد."
        )

        return

    await state.update_data(
        title=title
    )

    await state.set_state(
        AddSourceStates.description
    )

    await message.answer(
        """
📝 مرحله 2 از 4

توضیحات سورس را ارسال کنید:
""",
        reply_markup=admin_cancel()
    )


# =========================
# مرحله 2: توضیحات
# =========================

@router.message(AddSourceStates.description)
async def source_description(
    message: Message,
    state: FSMContext
):

    if not is_admin(message.from_user.id):

        return

    description = message.text.strip()

    if not description:

        await message.answer(
            "❌ توضیحات نمی‌تواند خالی باشد."
        )

        return

    await state.update_data(
        description=description
    )

    await state.set_state(
        AddSourceStates.price
    )

    await message.answer(
        """
🪙 مرحله 3 از 4

قیمت سورس را فقط به صورت عدد وارد کنید.

مثال:

50

یعنی 50 سکه.
""",
        reply_markup=admin_cancel()
    )


# =========================
# مرحله 3: قیمت
# =========================

@router.message(AddSourceStates.price)
async def source_price(
    message: Message,
    state: FSMContext
):

    if not is_admin(message.from_user.id):

        return

    try:

        price = int(message.text.strip())

    except (ValueError, AttributeError):

        await message.answer(
            "❌ قیمت باید فقط یک عدد باشد.\nمثلاً: 50"
        )

        return

    if price < 0:

        await message.answer(
            "❌ قیمت نمی‌تواند منفی باشد."
        )

        return

    await state.update_data(
        price=price
    )

    await state.set_state(
        AddSourceStates.file
    )

    await message.answer(
        """
📁 مرحله 4 از 4

حالا فایل سورس را به صورت فایل (Document) ارسال کنید.

⚠️ فایل را به صورت Document بفرستید، نه عکس.
""",
        reply_markup=admin_cancel()
    )


# =========================
# مرحله 4: فایل
# =========================

@router.message(AddSourceStates.file, F.document)
async def source_file(
    message: Message,
    state: FSMContext
):

    if not is_admin(message.from_user.id):

        return

    file_id = message.document.file_id

    data = await state.get_data()

    title = data.get("title")
    description = data.get("description")
    price = data.get("price")
    is_vip = data.get("is_vip", 0)

    source_id = await add_source(
        title=title,
        description=description,
        price=price,
        file_id=file_id,
        is_vip=is_vip
    )

    category = "👑 VIP" if is_vip else "🏆 برترین سورس‌ها"

    await state.clear()

    await message.answer(
        f"""
✅ سورس با موفقیت اضافه شد!

━━━━━━━━━━━━━━━━━━

📦 نام:
{title}

📝 توضیحات:
{description}

🪙 قیمت:
{price} سکه

📂 دسته:
{category}

🆔 شناسه سورس:
{source_id}

━━━━━━━━━━━━━━━━━━

🚀 سورس در لیست مربوطه قرار گرفت.
""",
        reply_markup=admin_menu()
    )


# =========================
# فایل اشتباه
# =========================

@router.message(AddSourceStates.file)
async def wrong_source_file(
    message: Message
):

    if not is_admin(message.from_user.id):

        return

    await message.answer(
        """
❌ لطفاً خود فایل سورس را به صورت Document ارسال کنید.

مثلاً فایل ZIP پروژه را ارسال کنید.
"""
    )


# =========================
# ❌ لغو
# =========================

@router.callback_query(F.data == "admin_cancel")
async def cancel_admin(
    callback: CallbackQuery,
    state: FSMContext
):

    if not is_admin(callback.from_user.id):

        await callback.answer(
            "⛔ دسترسی ندارید.",
            show_alert=True
        )

        return

    await state.clear()

    await callback.message.edit_text(
        """
👑 پنل مدیریت Nextel

عملیات لغو شد.
""",
        reply_markup=admin_menu()
    )

    await callback.answer()


# =========================
# 📋 لیست برترین سورس‌ها
# =========================

@router.callback_query(F.data == "admin_top_list")
async def admin_top_list(
    callback: CallbackQuery
):

    if not is_admin(callback.from_user.id):

        await callback.answer(
            "⛔ دسترسی ندارید.",
            show_alert=True
        )

        return

    sources = await get_sources(is_vip=0)

    if not sources:

        await callback.message.edit_text(
            """
📋 لیست برترین سورس‌ها

❌ هیچ سورسی وجود ندارد.
""",
            reply_markup=admin_menu()
        )

        await callback.answer()

        return

    text = "📋 لیست برترین سورس‌ها\n\n"

    for source in sources:

        source_id = source[0]
        title = source[1]
        price = source[3]

        text += (
            f"🆔 {source_id}\n"
            f"📦 {title}\n"
            f"🪙 {price} سکه\n"
            f"━━━━━━━━━━━━━━\n"
        )

    await callback.message.edit_text(
        text,
        reply_markup=admin_menu()
    )

    await callback.answer()


# =========================
# 👑 لیست VIP
# =========================

@router.callback_query(F.data == "admin_vip_list")
async def admin_vip_list(
    callback: CallbackQuery
):

    if not is_admin(callback.from_user.id):

        await callback.answer(
            "⛔ دسترسی ندارید.",
            show_alert=True
        )

        return

    sources = await get_sources(is_vip=1)

    if not sources:

        await callback.message.edit_text(
            """
👑 لیست سورس‌های VIP

❌ هیچ سورس VIP وجود ندارد.
""",
            reply_markup=admin_menu()
        )

        await callback.answer()

        return

    text = "👑 لیست سورس‌های VIP\n\n"

    for source in sources:

        source_id = source[0]
        title = source[1]
        price = source[3]

        text += (
            f"🆔 {source_id}\n"
            f"📦 {title}\n"
            f"🪙 {price} سکه\n"
            f"━━━━━━━━━━━━━━\n"
        )

    await callback.message.edit_text(
        text,
        reply_markup=admin_menu()
    )

    await callback.answer()


# =========================
# 🗑 حذف سورس
# =========================

@router.callback_query(F.data == "admin_delete_source")
async def admin_delete_source_menu(
    callback: CallbackQuery
):

    if not is_admin(callback.from_user.id):

        await callback.answer(
            "⛔ دسترسی ندارید.",
            show_alert=True
        )

        return

    sources = await get_sources(is_vip=0)

    vip_sources = await get_sources(is_vip=1)

    all_sources = sources + vip_sources

    if not all_sources:

        await callback.message.edit_text(
            """
🗑 حذف سورس

❌ هیچ سورسی برای حذف وجود ندارد.
""",
            reply_markup=admin_menu()
        )

        await callback.answer()

        return

    buttons = []

    for source in all_sources:

        source_id = source[0]
        title = source[1]
        is_vip = source[5]

        prefix = "👑" if is_vip else "📦"

        buttons.append([
            InlineKeyboardButton(
                text=f"{prefix} {title}",
                callback_data=f"delete_source:{source_id}"
            )
        ])

    buttons.append([
        InlineKeyboardButton(
            text="🔙 بازگشت",
            callback_data="admin_back"
        )
    ])

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=buttons
    )

    await callback.message.edit_text(
        """
🗑 حذف سورس

سورسی که می‌خواهید حذف کنید را انتخاب کنید:
""",
        reply_markup=keyboard
    )

    await callback.answer()


# =========================
# تأیید حذف
# =========================

@router.callback_query(
    F.data.startswith("delete_source:")
)
async def delete_source_confirm(
    callback: CallbackQuery
):

    if not is_admin(callback.from_user.id):

        await callback.answer(
            "⛔ دسترسی ندارید.",
            show_alert=True
        )

        return

    try:

        source_id = int(
            callback.data.split(":")[1]
        )

    except (ValueError, IndexError):

        await callback.answer(
            "❌ شناسه نامعتبر است.",
            show_alert=True
        )

        return

    sources = await get_sources(is_vip=0)
    vip_sources = await get_sources(is_vip=1)

    all_sources = sources + vip_sources

    selected = None

    for source in all_sources:

        if source[0] == source_id:

            selected = source
            break

    if selected is None:

        await callback.answer(
            "❌ سورس پیدا نشد.",
            show_alert=True
        )

        return

    title = selected[1]

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[

            [
                InlineKeyboardButton(
                    text="✅ بله، حذف کن",
                    callback_data=f"confirm_delete:{source_id}"
                )
            ],

            [
                InlineKeyboardButton(
                    text="❌ لغو",
                    callback_data="admin_delete_source"
                )
            ]

        ]
    )

    await callback.message.edit_text(
        f"""
⚠️ تأیید حذف

آیا مطمئن هستید که می‌خواهید این سورس را حذف کنید؟

📦 {title}

❗ این عملیات قابل برگشت نیست.
""",
        reply_markup=keyboard
    )

    await callback.answer()


# =========================
# حذف نهایی
# =========================

@router.callback_query(
    F.data.startswith("confirm_delete:")
)
async def confirm_delete(
    callback: CallbackQuery
):

    if not is_admin(callback.from_user.id):

        await callback.answer(
            "⛔ دسترسی ندارید.",
            show_alert=True
        )

        return

    try:

        source_id = int(
            callback.data.split(":")[1]
        )

    except (ValueError, IndexError):

        await callback.answer(
            "❌ شناسه نامعتبر است.",
            show_alert=True
        )

        return

    deleted = await delete_source(
        source_id
    )

    if deleted:

        await callback.message.edit_text(
            """
✅ سورس با موفقیت حذف شد.
""",
            reply_markup=admin_menu()
        )

        await callback.answer(
            "🗑 حذف شد."
        )

    else:

        await callback.answer(
            "❌ سورس پیدا نشد.",
            show_alert=True
        )


# =========================
# 🔙 بازگشت پنل
# =========================

@router.callback_query(F.data == "admin_back")
async def admin_back(
    callback: CallbackQuery
):

    if not is_admin(callback.from_user.id):

        await callback.answer(
            "⛔ دسترسی ندارید.",
            show_alert=True
        )

        return

    await callback.message.edit_text(
        """
👑 پنل مدیریت Nextel

یکی از گزینه‌های زیر را انتخاب کنید:
""",
        reply_markup=admin_menu()
    )

    await callback.answer()


# =========================
# 📊 آمار
# =========================

@router.callback_query(F.data == "admin_stats")
async def admin_stats(
    callback: CallbackQuery
):

    if not is_admin(callback.from_user.id):

        await callback.answer(
            "⛔ دسترسی ندارید.",
            show_alert=True
        )

        return

    normal_sources = await get_sources(is_vip=0)
    vip_sources = await get_sources(is_vip=1)

    total_sources = len(normal_sources)
    total_vip = len(vip_sources)

    await callback.message.edit_text(
        f"""
📊 آمار Nextel

━━━━━━━━━━━━━━━━━━

🏆 سورس‌های عادی:
{total_sources}

👑 سورس‌های VIP:
{total_vip}

📦 مجموع سورس‌ها:
{total_sources + total_vip}

━━━━━━━━━━━━━━━━━━
""",
        reply_markup=admin_menu()
    )

    await callback.answer()
