from aiogram import types

from dreamprf_diary_bot.services import users


async def register(message: types.Message):
    sid = users.register(message.from_user.id, message.text)
    if sid:
        await message.reply(f'Идентификатор таблицы сохранен: {sid}', reply=False)
    else:
        await message.reply('Для записи комментария к НП перейдите в режим /night и добавьте НП.')
