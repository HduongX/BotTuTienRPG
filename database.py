import aiosqlite

DB_PATH = "data/bot.db"

async def init_db():
    async with aiosqlite.connect(DB_PATH) as db:
        await db.executescript("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            xu INTEGER DEFAULT 0,
            xp INTEGER DEFAULT 0,
            sect_id INTEGER
        );

        CREATE TABLE IF NOT EXISTS items (
            item_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            description TEXT,
            price INTEGER,
            xp_bonus INTEGER
        );

        CREATE TABLE IF NOT EXISTS inventory (
            user_id INTEGER,
            item_id INTEGER,
            amount INTEGER,
            PRIMARY KEY (user_id, item_id)
        );

        CREATE TABLE IF NOT EXISTS sects (
            sect_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            leader_id INTEGER,
            xp INTEGER DEFAULT 0
        );
        """)
        await db.commit()