from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


# =========================
# منوی اصلی
# =========================

def main_menu():

    return InlineKeyboardMarkup(
        inline_keyboard=[

            [
                InlineKeyboardButton(
                    text="🏆 برترین سورس‌ها",
                    callback_data="top_sources"
                ),
                InlineKeyboardButton(
                    text="👑 سورس VIP",
                    callback_data="vip_sources"
                )
            ],

            [
                InlineKeyboardButton(
                    text="👤 حساب من",
                    callback_data="my_account"
                ),
                InlineKeyboardButton(
                    text="🎡 گردونه شانس",
                    callback_data="spin"
                )
            ],

            [
                InlineKeyboardButton(
                    text="🛠️ پشتیبانی",
                    callback_data="support"
                ),
                InlineKeyboardButton(
                    text="🤖 راهنما",
                    callback_data="help"
                )
            ],

            [
                InlineKeyboardButton(
                    text="📢 کانال 1",
                    callback_data="channel_1"
                ),
                InlineKeyboardButton(
                    text="👤 کانال 2",
                    callback_data="channel_2"
                )
            ]

        ]
    )


# =========================
# دکمه برگشت
# =========================

def back_button():

    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🔙 بازگشت",
                    callback_data="back_main"
                )
            ]
        ]
    )


# =========================
# خرید سورس
# =========================

def buy_source(source_id):

    return InlineKeyboardMarkup(
        inline_keyboard=[

            [
                InlineKeyboardButton(
                    text="🛒 خرید سورس",
                    callback_data=f"buy_source:{source_id}"
                )
            ],

            [
                InlineKeyboardButton(
                    text="🔙 بازگشت",
                    callback_data="back_sources"
                )
            ]

        ]
    )


# =========================
# پنل مدیریت
# =========================

def admin_menu():

    return InlineKeyboardMarkup(
        inline_keyboard=[

            [
                InlineKeyboardButton(
                    text="➕ اضافه کردن سورس",
                    callback_data="admin_add_source"
                )
            ],

            [
                InlineKeyboardButton(
                    text="👑 اضافه کردن سورس VIP",
                    callback_data="admin_add_vip"
                )
            ],

            [
                InlineKeyboardButton(
                    text="📋 لیست برترین سورس‌ها",
                    callback_data="admin_top_list"
                )
            ],

            [
                InlineKeyboardButton(
                    text="👑 لیست سورس‌های VIP",
                    callback_data="admin_vip_list"
                )
            ],

            [
                InlineKeyboardButton(
                    text="🗑 حذف سورس",
                    callback_data="admin_delete_source"
                )
            ],

            [
                InlineKeyboardButton(
                    text="📊 آمار ربات",
                    callback_data="admin_stats"
                )
            ]

        ]
    )


# =========================
# لغو عملیات ادمین
# =========================

def admin_cancel():

    return InlineKeyboardMarkup(
        inline_keyboard=[

            [
                InlineKeyboardButton(
                    text="❌ لغو",
                    callback_data="admin_cancel"
                )
            ]

        ]
    )
