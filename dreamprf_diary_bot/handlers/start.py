from aiogram import types

from dreamprf_diary_bot import static


async def start(message: types.Message):
    response = static.start_message
    await message.reply(response, reply=False)
