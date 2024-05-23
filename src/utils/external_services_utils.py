from src.consts import SCIENCE_PAPER_INFO_PATTERN
from src.external_service.models import WorkData


def get_papers_information(paper: WorkData) -> str:
    return SCIENCE_PAPER_INFO_PATTERN.format(
        link=paper.id,
        title=paper.title,
        abstract=paper.abstract,
        type=paper.type,
        year=paper.publication_date,
        cites=paper.cited_by_count,
        topic=paper.primary_topic.display_name,
        authors='\n'.join(item.name_plus_country for item in paper.authorships),
        sources=paper.best_oa_location.source.display_name
    )


