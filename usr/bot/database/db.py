import aiosqlite
import logging

class Database:
    def __init__(self, db_name='bot_database.db'):
        self.db_name = db_name

    async def connect(self):
        self.conn = await aiosqlite.connect(self.db_name)
        await self.create_tables()
        logging.info("Database connected")

    async def create_tables(self):
        await self.conn.execute('''CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            username TEXT,
            is_premium BOOLEAN DEFAULT FALSE,
            premium_end_date TIMESTAMP
        )''')
        await self.conn.execute('''CREATE TABLE IF NOT EXISTS admins (
            user_id INTEGER PRIMARY KEY
        )''')
        await self.conn.execute('''CREATE TABLE IF NOT EXISTS channels (
            channel_id INTEGER PRIMARY KEY,
            url TEXT,
            target_limit INTEGER,
            current_count INTEGER DEFAULT 0
        )''')
        await self.conn.execute('''CREATE TABLE IF NOT EXISTS anime_codes (
            code TEXT PRIMARY KEY
        )''')
        await self.conn.execute('''CREATE TABLE IF NOT EXISTS anime_files (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            code TEXT,
            file_id TEXT,
            description TEXT
        )''')
        await self.conn.commit()

db = Database()
