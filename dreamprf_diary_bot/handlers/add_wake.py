from aiogram import types
from aiogram.dispatcher import FSMContext

from dreamprf_diary_bot.services import night_register


async def add_wake(message: types.Message, state: FSMContext):
    added_time: str = night_register.add_wake(message.from_user.id)
    await state.update_data(last_night_time=added_time)
    await message.reply(f'Добавлено НП в {added_time}', reply=False)
