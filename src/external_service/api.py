import aiohttp

from src.consts import (AUTHORS_BY_NAME, FILTER_AUTHOR, FILTER_DATES,
                        FILTER_OA, FILTER_SOURCE, FILTER_TERMS, HOST,
                        SOURCES_BY_NAME)
from src.external_service.models import (AuthorsFilterResults,
                                         SourcesFilterResults,
                                         WorksFilterResults)


async def get_author_id(author_name: str):
    async with aiohttp.ClientSession() as session:
        async with session.get(f'{HOST}{AUTHORS_BY_NAME.format(author_name)}&per_page=1') as resp:
            json = await resp.json()
            return SourcesFilterResults(**json).results[0].id


async def get_source_id(source_name: str):
    async with aiohttp.ClientSession() as session:
        async with session.get(f'{HOST}{SOURCES_BY_NAME.format(source_name)}&per_page=1') as resp:
            # pprint.pprint(await resp.json())
            json = await resp.json()
            return AuthorsFilterResults(**json).results[0].id


class ExternalScienceAPI:

    async def get_works(
            self,
            terms: str = '',
            source_name: str = '',
            author_name: str = '',
            year_begin: int = '',
            year_end: int = '',
            pages_min: int = '',
            pages_max: int = ''
    ):
        author_id = (await get_author_id(author_name)).replace('https://openalex.org/',
                                                               '') if author_name else ''
        source_id = (await get_source_id(source_name)).replace('https://openalex.org/',
                                                               '') if source_name else ''
        date_begin, date_end = f'{year_begin}-01-01', f'{year_end}-12-31'
        async with aiohttp.ClientSession() as session:
            async with session.get(f'{HOST}/works?'
                                   f'{FILTER_TERMS.format(terms)}&'
                                   f'{FILTER_AUTHOR.format(author_id)}&'
                                   f'{FILTER_SOURCE.format(source_id)}&'
                                   f'{FILTER_DATES.format(date_begin, date_end)}&'
                                   f'{FILTER_OA.format(True)}&'
                                   f'per_page=10') as resp:

                json = await resp.json()
                partly_filtered_works = WorksFilterResults(**json).results
                filtered_works = []

                if pages_min and pages_max and pages_min <= pages_max:
                    for result in partly_filtered_works:
                        pages = result.biblio.page_count
                        if pages_min <= pages <= pages_max:
                            filtered_works.append(result)
                return partly_filtered_works if not filtered_works else filtered_works
