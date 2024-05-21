from src.consts import SCIENCE_PAPER_INFO_PATTERN
from src.external_service.models import WorksFilterResults


def get_papers_information(papers_models: WorksFilterResults) -> list[str]:
    papers = []
    for paper in papers_models:
        link = paper.id
        title = paper.title
        papers.append(SCIENCE_PAPER_INFO_PATTERN.format(link=link, title=title))
    return papers
#
#
# async def main():
#     api_service = ExternalScienceAPI()
#     papers_models = await api_service.get_works(year_begin=2010, year_end=2010)
#
#     papers = get_papers_information(papers_models=papers_models)
#
#
# asyncio.run(main())
