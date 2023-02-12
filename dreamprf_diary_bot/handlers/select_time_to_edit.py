from aiogram import types
from aiogram.dispatcher import FSMContext


async def select_time_to_edit(call: types.CallbackQuery, state: FSMContext):
    time_str = call.data.split('_', 2)[-1].replace('_', ':')
    await state.update_data(last_night_time=time_str)
    await call.message.reply(f'Введите новый комментарий для просыпания в {time_str}', reply=False)
    await call.answer()
