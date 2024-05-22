from aiogram.filters import BaseFilter
from aiogram.types import Message

from src.consts import (LOWER_BOUND_PAGES, LOWER_BOUND_YEARS, MAX_TERMS_COUNT,
                        PAGES_REGEX_PATTERN, TEXT_REGEX_PATTERN,
                        UPPER_BOUND_PAGES, UPPER_BOUND_YEARS,
                        YEARS_REGEX_PATTERN)
from src.utils.filters_utils import validate_numbers_span_call_parameters, validate_text_call_parameters


class TextSearchingParametersFilters(BaseFilter):
    async def __call__(self, message: Message) -> bool | dict[str, list[str]]:
        return validate_text_call_parameters(
            message=message,
            pattern=TEXT_REGEX_PATTERN,
            max_count_messages=MAX_TERMS_COUNT
        )


class YearsSearchingParametersFilters(BaseFilter):
    async def __call__(self, message: Message) -> bool | dict[str, list[int]]:
        return validate_numbers_span_call_parameters(
            message=message,
            pattern=YEARS_REGEX_PATTERN,
            lower_bound=LOWER_BOUND_YEARS,
            upper_bound=UPPER_BOUND_YEARS
        )


class PagesSearchingParametersFilters(BaseFilter):
    async def __call__(self, message: Message) -> bool | dict[str, list[int]]:
        return validate_numbers_span_call_parameters(
            message=message,
            pattern=PAGES_REGEX_PATTERN,
            lower_bound=LOWER_BOUND_PAGES,
            upper_bound=UPPER_BOUND_PAGES
        )
