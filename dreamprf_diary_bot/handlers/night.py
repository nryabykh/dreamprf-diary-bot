from aiogram import types
from aiogram.dispatcher import FSMContext

from dreamprf_diary_bot.services.night_register import NightRegister


async def night(message: types.Message, state: FSMContext):
    kb = [[types.KeyboardButton(text="Добавить НП")]]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        input_field_placeholder="Добавьте ночное пробуждение"
    )
    await message.answer("Включили режим записи ночных пробуждений.", reply_markup=keyboard)
    await state.set_state(NightRegister.start.state)
