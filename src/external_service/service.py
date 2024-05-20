import aiohttp
from src.external_service.models import SourcesFilterResults, AuthorsFilterResults, WorksFilterResults
from src.consts import *


class ExternalScienceAPI:

    async def get_author_id(self, author_name: str):
        async with aiohttp.ClientSession() as session:
            async with session.get(f'{HOST}{AUTHORS_BY_NAME.format(author_name)}&per_page=1') as resp:
                json = await resp.json()
                return SourcesFilterResults(**json).results[0].id

    async def get_source_id(self, source_name: str):
        async with aiohttp.ClientSession() as session:
            async with session.get(f'{HOST}{SOURCES_BY_NAME.format(source_name)}&per_page=1') as resp:
                # pprint.pprint(await resp.json())
                json = await resp.json()
                return AuthorsFilterResults(**json).results[0].id

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
        author_id = (await self.get_author_id(author_name)).replace('https://openalex.org/',
                                                                    '') if author_name else ''
        source_id = (await self.get_source_id(source_name)).replace('https://openalex.org/',
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


external_api = ExternalScienceAPI()
