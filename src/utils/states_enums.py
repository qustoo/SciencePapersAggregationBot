from enum import Enum


class StatesName(Enum):
    TERMS = 'terms'
    SOURCE_PUBLISHED = 'source_published'
    AUTHORS = 'authors'
    YEARS = ('min_years', 'max_years')
    PAGES = ('min_pages', 'max_pages')
