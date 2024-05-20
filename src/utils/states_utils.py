from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state

from src.database import db
from src.utils.enum_states import StatesName


async def upload_data_and_reset_state(user_id: int, state: FSMContext):
    state_data = await state.get_data()
    await db.insert_data(inserted_data=state_data, user_id=user_id)
    await state.set_state(default_state)


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
