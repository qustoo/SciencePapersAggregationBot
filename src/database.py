from typing import Optional

import aiosqlite


class AsyncBotDatabase:
    def __init__(self, filename_db: str):
        self.filename_db = filename_db

    async def execute(self, query: str, data: Optional[tuple] = None, fetchone: bool = False, commit: bool = False):
        returned_result = None
        async with aiosqlite.connect(self.filename_db) as _db:
            cursor = await _db.cursor()
            await cursor.execute(query, data)
            if commit:
                await _db.commit()
            if fetchone:
                returned_result = await cursor.fetchone()

            return returned_result

    async def create_table(self):
        await self.create_table_parameters()
        await self.create_table_page_information()

    async def create_table_parameters(self):
        query = """
              CREATE TABLE IF NOT EXISTS parameters( 
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

    async def create_table_page_information(self):
        query = """
              CREATE TABLE IF NOT EXISTS page_information( 
              id INTEGER PRIMARY KEY AUTOINCREMENT,
              user_id INTEGER,
              current_page INT,
              total_pages INT
              )
              """
        await self.execute(query=query, commit=True)

    async def drop_tables(self):
        query = """
        DROP TABLE IF EXISTS parameters
        DROP TABLE IF EXISTS page_information
        """
        await self.execute(query=query)

    async def insert_data(self, table_name: str, inserted_data: dict[str, str | int], user_id: int):
        columns = ', '.join(inserted_data.keys())
        marks = ', '.join('?' * len(inserted_data))
        query = "INSERT INTO %s(user_id, %s) VALUES (%d, %s)" % (table_name, columns, user_id, marks)
        await self.execute(query=query, data=tuple(inserted_data.values()), commit=True)

    async def update_data(self, table_name: str, updated_data: dict[str, str | int], user_id: int):
        columns = ', '.join(updated_data.keys())
        marks = ', '.join('?' * len(updated_data))
        query = "UPDATE %s SET %s = %s WHERE user_id = %d" % (table_name, columns, marks, user_id)
        await self.execute(query=query, data=tuple(updated_data.values()), commit=True)

    async def fetch_one_last_data(self, table_name: str, searching_columns: list[str], user_id: int):
        columns = ', '.join(searching_columns)
        query = """
        SELECT %s
        FROM %s 
        WHERE user_id = %d
        ORDER BY id DESC
        LIMIT 1
        """ % (columns, table_name, user_id)
        fetched_data = await self.execute(query=query, fetchone=True)
        return fetched_data
