import asyncpg
import os

class DatabaseConnection:
    def __init__(self):
        self.conn = None

    async def __aenter__(self):
        DATABASE_URL = os.environ.get("PGURL", "postgres://postgres:postgres@db:5432/estoque")
        self.conn = await asyncpg.connect(DATABASE_URL)
        return self.conn

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.conn:
            await self.conn.close()