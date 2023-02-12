from aiogram import types
from aiogram.dispatcher import FSMContext


async def end(message: types.Message, state: FSMContext):
    await message.reply(
        "Вышли из режима записи ночных пробуждений.", reply_markup=types.ReplyKeyboardRemove(), reply=False
    )
    await state.finish()
