from src.database import AsyncBotDatabase


async def add_papers_to_database(papers: list, database: AsyncBotDatabase, user_id: int) -> None:
    for paper in papers:
        await database.insert_data(
            table_name='papers',
            inserted_data={
                'link': paper.id,
                'doi': paper.doi,
                'title': paper.title,
                'abstract': paper.abstract,
                'type': paper.type,
                'publication_date': paper.publication_date,
                'cites': paper.cited_by_count,
                'topic': paper.topic,
                'authors': paper.authors_countries_info,
                'sources': paper.sources,
                'page_count': paper.biblio.page_count
            },
            user_id=user_id,
        )
