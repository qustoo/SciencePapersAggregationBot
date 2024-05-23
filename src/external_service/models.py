from typing import Optional

from pydantic import BaseModel, computed_field


class AuthorData(BaseModel):
    id: str


class AuthorsFilterResults(BaseModel):
    results: list[AuthorData]


class SourceData(BaseModel):
    id: str
    display_name: Optional[str] = None
    type: str


class SourcesFilterResults(BaseModel):
    results: Optional[list[SourceData]]


class AuthorshipData(BaseModel):
    author_position: str
    raw_author_name: str
    countries: list[str]

    @computed_field
    def name_plus_country(self) -> str:
        if len(self.countries) != 0:
            countries = ', '.join(self.countries)
            return f'{self.raw_author_name} ({countries})'

        return self.raw_author_name + ' (Unknown)'


class Biblio(BaseModel):
    first_page: Optional[str] = None
    last_page: Optional[str] = None

    @computed_field
    def page_count(self) -> int:
        if self.first_page and self.last_page: 
            try:
                return int(self.first_page) - int(self.last_page) + 1
            except ValueError:
                return 0
            
        return 0
    

class TopicData(BaseModel):
    id: str
    display_name: str


class OaLocationData(BaseModel):
    is_accepted: bool
    is_published: bool
    source: Optional[SourceData]


class WorkData(BaseModel):
    id: str  # адрес страницы на опеналексе
    doi: Optional[str]  # ссылка на пдф
    title: Optional[str]  # название
    type: str  # тип (статья, ревью и т.д.)
    publication_date: str  # дата в формате гггг-мм-дд
    has_fulltext: bool
    cited_by_count: int  # число цитирований
    primary_topic: Optional[TopicData]  # тема вытаскивается через .display_name
    authorships: list[AuthorshipData]  # тут из каждого автора доставай .name_plus_coutry
    best_oa_location: Optional[OaLocationData]  # доставай название источника через .source.display_name
    biblio: Optional[Biblio]  # хранит номера страниц
    abstract_inverted_index: Optional[dict[str, list[int]]]  # плохой абстракт

    @computed_field
    def abstract(self) -> str:  # хороший абстракт
        if self.abstract_inverted_index is not None:
            l_inv = [(w, p) for w, pos in self.abstract_inverted_index.items() for p in pos]
            sorted_map = map(lambda x: x[0], sorted(l_inv, key=lambda x: x[1]))
            return " ".join(sorted_map)


class WorksFilterResults(BaseModel):
    results: list[WorkData]
