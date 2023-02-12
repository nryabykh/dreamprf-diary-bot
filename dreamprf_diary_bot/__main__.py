import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.files import JSONStorage
from aiogram.dispatcher.filters import Text
from aiogram.types import BotCommand

from dreamprf_diary_bot import config, handlers
from dreamprf_diary_bot.handlers.states import NightRegister

logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

if not config.TELEGRAM_BOT_TOKEN:
    raise ValueError("TELEGRAM_BOT_TOKEN env variable should be initialized in .env.")


async def set_commands(bot: Bot):
    commands = [
        BotCommand(command="/start", description="Привет!"),
        BotCommand(command="/help", description="Справка по работе"),
        BotCommand(command="/night", description="Включить режим записи НП"),
        BotCommand(command="/last", description="Посмотреть и отредактировать НП последней ночи"),
        BotCommand(command="/end", description="Выйти из режима записи НП"),
    ]
    await bot.set_my_commands(commands)


async def main():
    bot = Bot(token=config.TELEGRAM_BOT_TOKEN)
    dp = Dispatcher(bot, storage=JSONStorage(config.STATE_PATH))

    command_handlers = {
        'start': handlers.start,
        'help': handlers.help_,
        'night': handlers.night,
        'end': handlers.end,
        'last': handlers.last,
    }

    text_handlers = [
        {'handler': handlers.add_wake, 'filters': [Text('Добавить НП')], 'state': NightRegister.start},
        {'handler': handlers.add_note, 'filters': [], 'state': NightRegister.start},
        {'handler': handlers.register, 'filters': [Text(startswith='https://docs.google.com')], 'state': '*'}
    ]

    callback_handlers = [
        {
            'handler': handlers.select_time_to_edit,
            'filters': [Text(startswith='edit_note_')],
            'state': NightRegister.start
        }
    ]

    for cmd_name, cmd_handler in command_handlers.items():
        dp.register_message_handler(cmd_handler, commands=cmd_name, state='*')

    for handler in text_handlers:
        dp.register_message_handler(handler['handler'], *handler['filters'], state=handler['state'])

    for handler in callback_handlers:
        dp.register_callback_query_handler(handler['handler'], *handler['filters'], state=handler['state'])

    await set_commands(bot)

    await dp.start_polling()


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except Exception:
        import traceback
        logger.warning(traceback.format_exc())
