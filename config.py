import os

BOT_TOKEN = os.getenv("BOT_TOKEN")

# آیدی عددی ادمین
ADMIN_ID = int(os.getenv("ADMIN_ID", "0"))

# کانالی که کاربر برای استفاده از ربات باید عضو آن باشد
REQUIRED_CHANNEL = os.getenv("REQUIRED_CHANNEL", "@YOUR_CHANNEL")

# لینک کانال اطلاع‌رسانی
CHANNEL_1_URL = os.getenv(
    "CHANNEL_1_URL",
    "https://t.me/YOUR_CHANNEL_1"
)

# لینک کانال شخصی
CHANNEL_2_URL = os.getenv(
    "CHANNEL_2_URL",
    "https://t.me/YOUR_CHANNEL_2"
)

# پشتیبانی
SUPPORT_USERNAME = "@Ya3in_1s"

if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN در Environment Variables تنظیم نشده است.")
