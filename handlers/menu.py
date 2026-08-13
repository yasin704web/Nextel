from aiogram import Router, F
from aiogram.types import CallbackQuery

from database import (
    get_user,
    get_purchase_count
)

from keyboards import (
    main_menu,
    back_button
)


router = Router()


# =========================
# 👤 حساب من
# =========================

@router.callback_query(F.data == "my_account")
async def my_account(callback: CallbackQuery):

    user_id = callback.from_user.id

    user = await get_user(user_id)

    if user is None:

        await callback.answer(
            "❌ حساب شما پیدا نشد.",
            show_alert=True
        )

        return

    purchases = await get_purchase_count(user_id)

    user_id_db = user[0]
    username = user[1]
    full_name = user[2]
    coins = user[3]

    if username:
        display_name = f"@{username}"
    else:
        display_name = full_name or "کاربر"

    text = f"""
👤 حساب کاربری | Nextel

سلام {display_name} 👋

━━━━━━━━━━━━━━━━━━

🪪 نام:
{full_name or "ثبت نشده"}

🆔 آیدی:
{user_id_db}

🪙 موجودی سکه:
{coins}

📦 تعداد سورس‌های خریداری‌شده:
{purchases}

━━━━━━━━━━━━━━━━━━

🚀 Nextel
سورس‌های آماده، ایده‌های بزرگ‌تر.
"""

    await callback.message.edit_text(
        text,
        reply_markup=back_button()
    )

    await callback.answer()


# =========================
# 🔙 بازگشت به منوی اصلی
# =========================

@router.callback_query(F.data == "back_main")
async def back_main(callback: CallbackQuery):

    text = """
🤖 Nextel

لطفاً یکی از گزینه‌های زیر را انتخاب کنید:
"""

    await callback.message.edit_text(
        text,
        reply_markup=main_menu()
    )

    await callback.answer()


# =========================
# 🛠️ پشتیبانی
# =========================

@router.callback_query(F.data == "support")
async def support(callback: CallbackQuery):

    text = """
🛠️ پشتیبانی رسمی | Nextel

سلام و خوش آمدید به بخش پشتیبانی Nextel 👋

اگر هنگام نصب، راه‌اندازی یا استفاده از سورس‌کد خریداری‌شده با مشکلی مواجه شدید، می‌توانید درخواست خود را از طریق پشتیبانی ارسال کنید.

📌 برای بررسی سریع‌تر، لطفاً مشکل خود را کامل و واضح توضیح دهید.

💻 اگر با خطا مواجه شده‌اید، متن خطا یا اسکرین‌شات آن را نیز ارسال کنید.

📦 حتماً نام سورس‌کد یا محصولی که در رابطه با آن مشکل دارید را ذکر کنید.

🔧 مشکلات مربوط به نصب، تنظیمات، اجرا و پیکربندی تا حد امکان توسط تیم پشتیبانی بررسی می‌شوند.

🔐 اطلاعات حساس مانند رمز عبور، توکن ربات یا اطلاعات ورود خود را ارسال نکنید.

⏱️ درخواست‌ها به ترتیب بررسی می‌شوند؛ بنابراین از ارسال چندین پیام پشت‌سرهم خودداری کنید.

❤️ Nextel؛ همراه شما در مسیر ساخت و توسعه پروژه‌های حرفه‌ای

👨‍💻 پشتیبانی:
@Ya3in_1s
"""

    await callback.message.edit_text(
        text,
        reply_markup=back_button()
    )

    await callback.answer()


# =========================
# 🤖 راهنما
# =========================

@router.callback_query(F.data == "help")
async def help_handler(callback: CallbackQuery):

    text = """
🤖 راهنمای کامل ربات فروش سورس کد Nextel

سلام! 👋

من Nextel هستم؛ ربات فروش سورس‌کد و محصولات برنامه‌نویسی.

در این ربات می‌توانید سورس‌های آماده را مشاهده کنید، مشخصات محصولات را ببینید و با استفاده از سکه‌های خود سورس موردنظر را تهیه کنید.

━━━━━━━━━━━━━━━━━━

🛒 خرید سورس

از بخش «برترین سورس‌ها» یا «سورس VIP» محصول موردنظر را انتخاب کنید.

بعد از انتخاب محصول، قیمت آن نمایش داده می‌شود.

اگر سکه کافی داشته باشید، مبلغ از حساب شما کسر شده و فایل سورس برایتان ارسال می‌شود.

━━━━━━━━━━━━━━━━━━

👤 حساب من

در این بخش می‌توانید:

🪙 موجودی سکه
📦 تعداد سورس‌های خریداری‌شده
🪪 نام و اطلاعات حساب

را مشاهده کنید.

━━━━━━━━━━━━━━━━━━

🎡 گردونه شانس

با استفاده از گردونه می‌توانید شانس خود را امتحان کنید.

ممکن است برنده سکه شوید یا نتیجه‌ای دریافت نکنید.

━━━━━━━━━━━━━━━━━━

👑 سورس VIP

در این بخش سورس‌های ویژه قرار می‌گیرند.

قیمت محصولات VIP با سکه مشخص می‌شود.

━━━━━━━━━━━━━━━━━━

🛠️ پشتیبانی

اگر در نصب یا استفاده از سورس خریداری‌شده مشکلی داشتید، با پشتیبانی در ارتباط باشید:

@Ya3in_1s

━━━━━━━━━━━━━━━━━━

🚀 Nextel
سورس‌های آماده، ایده‌های بزرگ‌تر.
"""

    await callback.message.edit_text(
        text,
        reply_markup=back_button()
    )

    await callback.answer()


# =========================
# 📢 کانال 1
# =========================

@router.callback_query(F.data == "channel_1")
async def channel_1(callback: CallbackQuery):

    await callback.answer(
        "📢 کانال اطلاع‌رسانی Nextel",
        show_alert=True
    )


# =========================
# 👤 کانال 2
# =========================

@router.callback_query(F.data == "channel_2")
async def channel_2(callback: CallbackQuery):

    await callback.answer(
        "👤 کانال شخصی Nextel",
        show_alert=True
    )
