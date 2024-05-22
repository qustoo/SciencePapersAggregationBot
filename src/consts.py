START_MESSAGE = 'Привет!\nЭтот бот умеет агрегировать информацию из различных источников!'
HELP_MESSAGE = 'Привет!\nСкоро тут будет будет инфа по помощи!'
LOGGING_FORMAT = '[%(asctime)s] #%(levelname)-8s %(filename)s:%(lineno)d - %(name)s - %(message)s'
LOWER_BOUND_YEARS = 1970
UPPER_BOUND_YEARS = 2024
TEXT_REGEX_PATTERN = r'\b[^\d\W]+\b'
YEARS_REGEX_PATTERN = r'\b(?:19|20)\d{2}(?:-(?:19|20)\d{2})?'
PAGES_REGEX_PATTERN = r'\b(?:[1-9])\d{0,2}(?:-(?:[1-9])\d{0,2})?'
MAX_TERMS_COUNT = 20
LOWER_BOUND_PAGES = 0
UPPER_BOUND_PAGES = 250
PARAMETER_NOT_SET = '[ДАННЫЕ ОТСУТСТВУЮТ]'
HOST = 'https://api.openalex.org'
AUTHORS_BY_NAME = '/autocomplete/authors?q={}'
SOURCES_BY_NAME = '/autocomplete/sources?q={}'
FILTER_TERMS = 'abstract.search:{}'
FILTER_DATES = 'from_publication_date:{},to_publication_date:{}'
FILTER_AUTHOR = 'authorships.author.id:{}'
FILTER_SOURCE = 'best_oa_location.source.id:{}'
FILTER_OA = 'open_access.is_oa:{}'
SCIENCE_PAPER_INFO_PATTERN = """
Link = {link}
Title = {title}
"""
ENTERED_PARAMETERS_PATTERN = """
Ключевые слова: %s\n
Журнал/издание: %s\n
Авторы: {%s}\n
Год выпуска: от %s до %s\n
Количество страниц: от %s до %s\n
"""
