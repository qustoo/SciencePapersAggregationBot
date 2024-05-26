from dataclasses import dataclass

from src.consts import SCIENCE_PAPER_INFO_PATTERN
from src.external_service.models import WorkData


@dataclass
class PaperData:
    representation: str
    link: str


def get_papers_representation(papers: list[WorkData | tuple]) -> list[PaperData]:
    papers_data = []
    for paper in papers:
        if isinstance(paper, WorkData):
            papers_data.append(PaperData(
                representation=SCIENCE_PAPER_INFO_PATTERN.format(
                    paper.id,
                    paper.doi,
                    paper.title,
                    paper.abstract,
                    paper.type,
                    paper.publication_date,
                    paper.cited_by_count,
                    paper.topic,
                    paper.authors_countries_info,
                    paper.sources,
                    paper.biblio.page_count
                ),
                link=paper.id
            ))
        elif isinstance(paper, tuple):
            paper_link, *paper_other_data = paper
            papers_data.append(PaperData(
                representation=SCIENCE_PAPER_INFO_PATTERN.format(paper_link, *paper_other_data),
                link=paper_link,
            ))
    return papers_data
