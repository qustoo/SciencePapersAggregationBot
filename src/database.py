from typing import Optional

import aiosqlite

from src.config import FILENAME_DATABASE


class AsyncBotDatabase:
    def __init__(self, filename_db: str):
        self.filename_db = filename_db

    async def execute(
            self,
            query: str,
            data: Optional[tuple] = None,
            fetchone: bool = False,
            fetchall: bool = False,
            commit: bool = False):
        returned_result = None
        async with aiosqlite.connect(self.filename_db) as _db:
            cursor = await _db.cursor()
            await cursor.execute(query, data)
            if commit:
                await _db.commit()
            if fetchone:
                returned_result = await cursor.fetchone()
            if fetchall:
                returned_result = await cursor.fetchall()

            return returned_result

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

    async def create_table_papers(self):
        query = """
              CREATE TABLE IF NOT EXISTS papers( 
              id INTEGER PRIMARY KEY AUTOINCREMENT,
              user_id INTEGER,
              link TEXT,
              doi TEXT,
              title TEXT,
              abstract TEXT,
              publication_date TEXT,
              cites INT,
              topic TEXT,
              authors TEXT,
              sources TEXT
              )
              """
        await self.execute(query=query, commit=True)

    async def create_table_bookmarks(self):
        query = """
              CREATE TABLE IF NOT EXISTS bookmarks( 
              id INTEGER PRIMARY KEY AUTOINCREMENT,
              user_id INTEGER,
              paper_id INT,
              FOREIGN KEY(paper_id) REFERENCES papers(id)
              )
              """
        await self.execute(query=query, commit=True)

    async def create_tables(self):
        await self.create_table_parameters()
        await self.create_table_page_information()
        await self.create_table_papers()
        await self.create_table_bookmarks()

    async def drop_tables(self):
        query = """
        DROP TABLE IF EXISTS parameters
        DROP TABLE IF EXISTS page_information        
        DROP TABLE IF EXISTS papers
        DROP TABLE IF EXISTS bookmarks
        """
        await self.execute(query=query, commit=True)

    async def insert_data(self, table_name: str, inserted_data: dict[str, str | int], user_id: int):
        columns = ', '.join(inserted_data.keys())
        marks = ', '.join('?' * len(inserted_data))
        query = "INSERT INTO %s(user_id, %s) VALUES (%d, %s)" % (table_name, columns, user_id, marks)
        await self.execute(query=query, data=tuple(inserted_data.values()), commit=True)

    async def update_data(self, table_name: str, updated_data: dict[str, str | int], user_id: int):
        set_data = ', '.join([f'{key} = ?' for key in updated_data.keys()])
        query = "UPDATE %s SET %s WHERE user_id = %d" % (table_name, set_data, user_id)
        await self.execute(query=query, data=tuple(updated_data.values()), commit=True)

    async def fetch_data(
            self,
            table_name: str,
            searching_columns: list[str],
            filter_columns: dict[str, str | int],
            fetchone: bool = False,
            fetchall: bool = False,
    ):
        columns = ', '.join(searching_columns)
        filters = ' and '.join([f'{key} = ?' for key in filter_columns.keys()])
        query = """
        SELECT %s
        FROM %s
        WHERE %s
        ORDER BY id DESC
        """ % (columns, table_name, filters)
        fetched_data = await self.execute(
            query=query,
            data=tuple(filter_columns.values()),
            fetchone=fetchone,
            fetchall=fetchall,
        )
        return fetched_data

    async def remove_data(self, table_name: str, removed_data: dict[str, str | int]):
        conditions = ' and '.join(f'{key} = ?' for key in removed_data.keys())
        query = """
        DELETE FROM %s
        WHERE %s
        """ % (table_name, conditions)
        await self.execute(query=query, data=tuple(removed_data.values()), commit=True)

    async def fetch_user_bookmarks_data(self, user_id: int):
        query = """
        SELECT papers.link, papers.title
        FROM bookmarks
        JOIN papers on  bookmarks.paper_id = papers.id
        WHERE bookmarks.user_id = ?
        """
        fetched_data = await self.execute(query=query, data=(user_id,), fetchall=True)
        return fetched_data


db = AsyncBotDatabase(FILENAME_DATABASE)
