from src.database import AsyncBotDatabase


async def add_papers_to_database(papers: list, database: AsyncBotDatabase, user_id: int) -> None:
    for paper in papers:
        await database.insert_data(
            table_name='papers',
            # внести все параметры
            inserted_data={'link': paper.id, 'title': paper.title},
            user_id=user_id,
        )
