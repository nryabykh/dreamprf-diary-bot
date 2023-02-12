from aiogram import types
from aiogram.dispatcher import FSMContext

from dreamprf_diary_bot.services import night_register


async def add_note(message: types.Message, state: FSMContext):
    stored_data = await state.get_data()
    selected_wake_time: str = stored_data.get('last_night_time', None)
    added_time: str = night_register.add_note(message.from_user.id, message.text, selected_wake_time)
    await message.reply(f'Добавили комментарий к просыпанию в {added_time}', reply=False)
