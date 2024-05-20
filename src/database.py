from typing import Optional

import aiosqlite

from src.config import FILENAME_DATABASE


class AsyncBotDatabase:
    def __init__(self, filename_db=FILENAME_DATABASE):
        self.filename_db = filename_db

    async def execute(self, query: str, data: Optional[tuple] = None, fetchone: bool = False, commit: bool = False):
        returned_result = None
        async with aiosqlite.connect(self.filename_db) as db:
            cursor = await db.cursor()
            await cursor.execute(query, data)
            if commit:
                await db.commit()
            if fetchone:
                returned_result = await cursor.fetchone()

            return returned_result

    async def create_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS science_paper_parameters( 
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        terms TEXT,
        source_published TEXT,
        authors TEXT,
        min_years INT,
        max_years INT,
        min_pages INT,
        max_pages INT
        )
        """
        await self.execute(query=query, commit=True)

    async def drop_table(self):
        query = """
        DROP TABLE IF EXISTS science_paper_parameters
        """
        await self.execute(query=query)

    async def insert_data(self, inserted_data: dict[str, str | int], user_id: int):
        columns = ', '.join(inserted_data.keys())
        marks = ', '.join('?' * len(inserted_data))
        query = "INSERT INTO science_paper_parameters(user_id, %s) VALUES (%d, %s)" % (columns, user_id, marks)
        await self.execute(query=query, data=tuple(inserted_data.values()), commit=True)

    async def fetch_last_entered_parameters(self, user_id: int):
        query = """
        SELECT terms, source_published, authors, min_years, max_years, min_pages, max_pages
        FROM science_paper_parameters 
        WHERE user_id = %d
        ORDER BY id
        LIMIT 1
        """ % user_id
        fetched_data = await self.execute(query=query, fetchone=True)
        return fetched_data


db = AsyncBotDatabase()
