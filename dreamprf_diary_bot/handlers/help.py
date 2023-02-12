from aiogram import types

from dreamprf_diary_bot import static


async def help_(message: types.Message):
    response = static.help_message
    await message.reply(response, reply=False)
