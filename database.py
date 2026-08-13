import aiosqlite

DB_NAME = "nextel.db"


async def init_db():
    async with aiosqlite.connect(DB_NAME) as db:

        await db.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                username TEXT,
                coins INTEGER DEFAULT 0,
                last_spin TEXT
            )
        """)

        await db.execute("""
            CREATE TABLE IF NOT EXISTS top_sources (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT,
                price TEXT,
                file_id TEXT
            )
        """)

        await db.commit()


async def add_user(user_id, username):
    async with aiosqlite.connect(DB_NAME) as db:

        await db.execute("""
            INSERT OR IGNORE INTO users
            (user_id, username, coins)
            VALUES (?, ?, 0)
        """, (user_id, username))

        await db.execute("""
            UPDATE users
            SET username = ?
            WHERE user_id = ?
        """, (username, user_id))

        await db.commit()


async def get_coins(user_id):
    async with aiosqlite.connect(DB_NAME) as db:

        cursor = await db.execute(
            "SELECT coins FROM users WHERE user_id = ?",
            (user_id,)
        )

        row = await cursor.fetchone()

        return row[0] if row else 0


async def add_coin(user_id):
    async with aiosqlite.connect(DB_NAME) as db:

        await db.execute("""
            UPDATE users
            SET coins = coins + 1
            WHERE user_id = ?
        """, (user_id,))

        await db.commit()


async def get_last_spin(user_id):
    async with aiosqlite.connect(DB_NAME) as db:

        cursor = await db.execute(
            "SELECT last_spin FROM users WHERE user_id = ?",
            (user_id,)
        )

        row = await cursor.fetchone()

        return row[0] if row else None


async def update_last_spin(user_id, date):
    async with aiosqlite.connect(DB_NAME) as db:

        await db.execute("""
            UPDATE users
            SET last_spin = ?
            WHERE user_id = ?
        """, (date, user_id))

        await db.commit()


async def add_source(title, description, price, file_id):
    async with aiosqlite.connect(DB_NAME) as db:

        await db.execute("""
            INSERT INTO top_sources
            (title, description, price, file_id)
            VALUES (?, ?, ?, ?)
        """, (
            title,
            description,
            price,
            file_id
        ))

        await db.commit()


async def get_sources():
    async with aiosqlite.connect(DB_NAME) as db:

        cursor = await db.execute("""
            SELECT id, title, description, price, file_id
            FROM top_sources
            ORDER BY id DESC
        """)

        return await cursor.fetchall()
