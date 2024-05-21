import re

from aiogram.types import Message


def filter_input_searching_parameters(pattern: str, message_text: str) -> bool | list[str]:
    return re.findall(pattern=pattern, string=message_text)


def validate_text_call_parameters(message: Message, pattern: str, max_count_messages: int):
    filtered_data = filter_input_searching_parameters(pattern=pattern, message_text=message.text)
    if not filtered_data or len(filtered_data) > max_count_messages:
        return False
    return {'valid_parameters': filtered_data}


def validate_numbers_span_call_parameters(message: Message, pattern: str, lower_bound: int, upper_bound: int):
    filtered_parameters = filter_input_searching_parameters(pattern=pattern, message_text=message.text)
    if not filtered_parameters:
        return False
    parameters = filtered_parameters[0]
    if '-' in parameters:
        lower_bound_parameter, upper_bound_parameter = list(map(int, sorted(parameters.split('-'))))
    else:
        lower_bound_parameter = upper_bound_parameter = int(parameters)

    if lower_bound >= lower_bound_parameter or upper_bound_parameter >= upper_bound:
        return False
    return {'valid_parameters': [lower_bound_parameter, upper_bound_parameter]}
