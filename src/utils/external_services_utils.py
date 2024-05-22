from src.consts import SCIENCE_PAPER_INFO_PATTERN
from src.external_service.models import WorkData


def get_papers_information(paper: WorkData) -> str:
    return SCIENCE_PAPER_INFO_PATTERN.format(link=paper.id, title=paper.title)
