from typing import Optional

from pydantic import BaseModel, computed_field, Field


class AuthorData(BaseModel):
    id: str


class AuthorsFilterResults(BaseModel):
    results: list[AuthorData]


class SourceData(BaseModel):
    id: str
    display_name: Optional[str] = None
    type: Optional[str] = 'no type provided'


class SourcesFilterResults(BaseModel):
    results: Optional[list[SourceData]]


class AuthorshipData(BaseModel):
    author_position: str
    raw_author_name: str
    countries: list[str]

    @computed_field
    @property
    def name_plus_country(self) -> str:
        countries = ', '.join(self.countries) or ' (Unknown country)'
        return f'{self.raw_author_name} ({countries})'


class Biblio(BaseModel):
    first_page: Optional[str] = None
    last_page: Optional[str] = None

    @computed_field
    @property
    def page_count(self) -> int:
        try:
            page_count = int(self.last_page) - int(self.first_page)
        except (ValueError, TypeError):
            page_count = 0
        return page_count


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
    type: Optional[str] = 'no type provided' # тип (статья, ревью и т.д.)
    publication_date: str  # дата в формате гггг-мм-дд
    has_fulltext: bool
    cited_by_count: int  # число цитирований
    primary_topic: Optional[TopicData]  # тема вытаскивается через .display_name
    authorships: list[AuthorshipData]  # тут из каждого автора доставай .name_plus_coutry
    best_oa_location: Optional[OaLocationData]  # доставай название источника через .source.display_name
    biblio: Optional[Biblio]  # хранит номера страниц
    abstract_inverted_index: Optional[dict[str, list[int]]]  # плохой абстракт

    @computed_field
    @property
    def abstract(self) -> str:  # хороший абстракт
        if self.abstract_inverted_index is not None:
            l_inv = [(w, p) for w, pos in self.abstract_inverted_index.items() for p in pos]
            sorted_map = map(lambda x: x[0], sorted(l_inv, key=lambda x: x[1]))
            return " ".join(sorted_map)

    @computed_field
    @property
    def authors_countries_info(self) -> str:
        return '\n'.join(item.name_plus_country for item in self.authorships)

    @computed_field
    @property
    def sources(self) -> str:
        oa_location = self.best_oa_location
        if oa_location and oa_location.source and oa_location.source.display_name:
            return oa_location.source.display_name
        return 'no sources'

    @computed_field
    @property
    def topic(self) -> str:
        primary_topic = self.primary_topic
        if primary_topic and primary_topic.display_name:
            return primary_topic.display_name
        return 'no topics'
class WorksFilterResults(BaseModel):
    results: list[WorkData]
