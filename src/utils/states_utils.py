from enum import Enum

from aiogram.fsm.context import FSMContext


class StatesName(Enum):
    TERMS = 'terms'
    SOURCE_PUBLISHED = 'source_published'
    AUTHORS = 'authors'
    YEARS = ('min_years', 'max_years')
    PAGES = ('min_pages', 'max_pages')


async def update_state_data(state_name: StatesName, concatenated: bool, parameters: list[str | int], state: FSMContext):
    state_data = await state.get_data()
    if concatenated:
        concatenate_new_parameters = ' '.join(parameters)
        if state_name.value not in state_data:
            await state.set_data(data={state_name.value: concatenate_new_parameters})
        else:
            concatenate_all_state_data = state_data[state_name.value] + concatenate_new_parameters
            state_data[state_name.value] = concatenate_all_state_data
            await state.set_data(data=state_data)
    else:
        first_value_parameter, second_value_parameter = parameters
        first_name_parameter, second_name_parameter = state_name.value
        state_data[first_name_parameter] = first_value_parameter
        state_data[second_name_parameter] = second_value_parameter
        await state.set_data(data=state_data)
