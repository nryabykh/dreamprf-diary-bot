from aiogram import types
from aiogram.dispatcher import FSMContext

from dreamprf_diary_bot.services import night_register


async def last(message: types.Message):
    times_and_notes: list[str] = night_register.get_all_wake_times_and_notes(message.from_user.id)
    keyboard = types.InlineKeyboardMarkup()
    for tn in times_and_notes:
        time_str = tn.split(' - ')[0]
        keyboard.add(types.InlineKeyboardButton(text=tn, callback_data=f'edit_note_{time_str.replace(":", "_")}'))

    await message.answer("Выберите НП для исправления комментария", reply_markup=keyboard)
