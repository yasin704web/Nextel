from aiogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton
)

from config import CHANNEL_1_URL, CHANNEL_2_URL


def join_keyboard():

    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="📢 عضویت در کانال",
                    url=CHANNEL_1_URL
                )
            ],
            [
                InlineKeyboardButton(
                    text="✅ بررسی عضویت",
                    callback_data="check_join"
                )
            ]
        ]
    )


def main_keyboard():

    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🏆 برترین سورس‌ها",
                    callback_data="top_sources"
                )
            ],
            [
                InlineKeyboardButton(
                    text="👑 سورس VIP",
                    callback_data="vip_sources"
                )
            ],
            [
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
                    callback_data="guide"
                )
            ],
            [
                InlineKeyboardButton(
                    text="📢 کانال ۱",
                    url=CHANNEL_1_URL
                ),
                InlineKeyboardButton(
                    text="👤 کانال ۲",
                    url=CHANNEL_2_URL
                )
            ]
        ]
    )


def admin_keyboard():

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
                    text="📋 لیست برترین سورس‌ها",
                    callback_data="top_sources"
                )
            ]
        ]
    )


def back_keyboard():

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
