from typing import Optional

from pydantic import BaseModel, computed_field


class AuthorData(BaseModel):
    id: str


class AuthorsFilterResults(BaseModel):
    results: list[AuthorData]


class SourceData(BaseModel):
    id: str


class SourcesFilterResults(BaseModel):
    results: list[SourceData]


class AuthorshipData(BaseModel):
    author_position: str  # first
    countries: list[str]  # [0]


class Biblio(BaseModel):
    first_page: Optional[str] = None
    last_page: Optional[str] = None
    #page_count: Optional[int] = None

    @computed_field
    def page_count(self) -> int:
        if self.first_page and self.last_page:
            return int(self.last_page) - int(self.first_page)
        return 0


class WorkData(BaseModel):
    id: str
    title: str
    type: str
    has_fulltext: bool
    authorships: list[AuthorshipData]
    biblio: Biblio


class WorksFilterResults(BaseModel):
    results: list[WorkData]
