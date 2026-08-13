import aiosqlite
from datetime import date


DB_NAME = "nextel.db"


# =========================
# راه‌اندازی دیتابیس
# =========================

async def init_db():

    async with aiosqlite.connect(DB_NAME) as db:

        await db.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                username TEXT,
                full_name TEXT,
                coins INTEGER DEFAULT 0,
                last_spin TEXT
            )
        """)

        await db.execute("""
            CREATE TABLE IF NOT EXISTS sources (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT,
                price INTEGER NOT NULL,
                file_id TEXT NOT NULL,
                is_vip INTEGER DEFAULT 0
            )
        """)

        await db.execute("""
            CREATE TABLE IF NOT EXISTS purchases (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                source_id INTEGER NOT NULL,
                price INTEGER NOT NULL,
                purchased_at TEXT NOT NULL
            )
        """)

        await db.commit()


# =========================
# کاربران
# =========================

async def add_user(
    user_id,
    username=None,
    full_name=None
):

    async with aiosqlite.connect(DB_NAME) as db:

        await db.execute("""
            INSERT INTO users
            (user_id, username, full_name, coins)
            VALUES (?, ?, ?, 0)

            ON CONFLICT(user_id)
            DO UPDATE SET
                username = excluded.username,
                full_name = excluded.full_name
        """, (
            user_id,
            username,
            full_name
        ))

        await db.commit()


async def get_user(user_id):

    async with aiosqlite.connect(DB_NAME) as db:

        cursor = await db.execute("""
            SELECT
                user_id,
                username,
                full_name,
                coins,
                last_spin
            FROM users
            WHERE user_id = ?
        """, (user_id,))

        return await cursor.fetchone()


# =========================
# سکه
# =========================

async def get_coins(user_id):

    user = await get_user(user_id)

    if user is None:
        return 0

    return user[3]


async def add_coin(
    user_id,
    amount=1
):

    async with aiosqlite.connect(DB_NAME) as db:

        await db.execute("""
            UPDATE users
            SET coins = coins + ?
            WHERE user_id = ?
        """, (
            amount,
            user_id
        ))

        await db.commit()


async def remove_coins(
    user_id,
    amount
):

    async with aiosqlite.connect(DB_NAME) as db:

        cursor = await db.execute("""
            UPDATE users
            SET coins = coins - ?
            WHERE user_id = ?
              AND coins >= ?
        """, (
            amount,
            user_id,
            amount
        ))

        await db.commit()

        return cursor.rowcount > 0


# =========================
# گردونه شانس
# =========================

async def get_last_spin(user_id):

    user = await get_user(user_id)

    if user is None:
        return None

    return user[4]


async def update_last_spin(
    user_id,
    spin_date
):

    async with aiosqlite.connect(DB_NAME) as db:

        await db.execute("""
            UPDATE users
            SET last_spin = ?
            WHERE user_id = ?
        """, (
            spin_date,
            user_id
        ))

        await db.commit()


# =========================
# سورس‌ها
# =========================

async def add_source(
    title,
    description,
    price,
    file_id,
    is_vip=0
):

    async with aiosqlite.connect(DB_NAME) as db:

        cursor = await db.execute("""
            INSERT INTO sources
            (
                title,
                description,
                price,
                file_id,
                is_vip
            )
            VALUES (?, ?, ?, ?, ?)
        """, (
            title,
            description,
            price,
            file_id,
            is_vip
        ))

        await db.commit()

        return cursor.lastrowid


async def get_sources(
    is_vip=0
):

    async with aiosqlite.connect(DB_NAME) as db:

        cursor = await db.execute("""
            SELECT
                id,
                title,
                description,
                price,
                file_id,
                is_vip
            FROM sources
            WHERE is_vip = ?
            ORDER BY id DESC
        """, (
            is_vip,
        ))

        return await cursor.fetchall()


async def get_source(
    source_id
):

    async with aiosqlite.connect(DB_NAME) as db:

        cursor = await db.execute("""
            SELECT
                id,
                title,
                description,
                price,
                file_id,
                is_vip
            FROM sources
            WHERE id = ?
        """, (
            source_id,
        ))

        return await cursor.fetchone()


async def delete_source(
    source_id
):

    async with aiosqlite.connect(DB_NAME) as db:

        cursor = await db.execute("""
            DELETE FROM sources
            WHERE id = ?
        """, (
            source_id,
        ))

        await db.commit()

        return cursor.rowcount > 0


# =========================
# خریدها
# =========================

async def add_purchase(
    user_id,
    source_id,
    price
):

    async with aiosqlite.connect(DB_NAME) as db:

        await db.execute("""
            INSERT INTO purchases
            (
                user_id,
                source_id,
                price,
                purchased_at
            )
            VALUES (?, ?, ?, ?)
        """, (
            user_id,
            source_id,
            price,
            date.today().isoformat()
        ))

        await db.commit()


async def get_purchase_count(
    user_id
):

    async with aiosqlite.connect(DB_NAME) as db:

        cursor = await db.execute("""
            SELECT COUNT(*)
            FROM purchases
            WHERE user_id = ?
        """, (
            user_id,
        ))

        result = await cursor.fetchone()

        return result[0]
