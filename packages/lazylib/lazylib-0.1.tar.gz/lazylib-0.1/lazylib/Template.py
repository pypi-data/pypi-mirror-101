import os
import sys


class Templates:
    def __init__(self, NEW_DIRS_FOR_TG: list = None, NEW_FILES_FOR_TG: list = None):
        self.__NEW_DIRS_FOR_TG = NEW_DIRS_FOR_TG
        self.__NEW_FILES_FOR_TG = NEW_FILES_FOR_TG

    def telegram_bot_template(self):
        """
        Создает архитектуру проекта под бота в Telegram.
        Архитектуру можно менять путем добавления новых директорий и файлов в атрибуты.
        :return:
        """
        if self.__NEW_DIRS_FOR_TG:
            for dr in self.__NEW_DIRS_FOR_TG:
                self.__maps.TELEGRAM.append(dr)
        self.__dirs_templates(self.__maps.TELEGRAM)
        self.__files_templates(self.__maps.TELEGRAM_FILES)
        os.system('pip install -r requirements.txt')

    def __dirs_templates(self, map):
        for dr in map:
            os.makedirs(dr, exist_ok=True)

    def __files_templates(self, map):
        for file in map:
            if isinstance(file, (dict)):
                for key, item in file.items():
                    with open(key, 'w') as f:
                        f.writelines([i + "\n" for i in file[key]])
                        f.close()
            else:
                with open(file, "w") as f:
                    f.close()

    class __maps(object):
        TELEGRAM = ['data', 'filters',
                    'handlers/channels', 'handlers/errors', 'handlers/groups', 'handlers/users',
                    'keyboards/inline', 'keyboards/default',
                    'middlewares', 'states',
                    'utils/misc', 'utils/redis']

        TELEGRAM_FILES = ['data/__init__.py',
                          {'data/config.py': ['import os',
                                              'from dotenv import load_dotenv',
                                              '',
                                              'load_dotenv()',
                                              f'BOT_TOKEN = str(os.getenv("BOT_TOKEN"))',
                                              'admins = [',
                                              '',
                                              ']',
                                              '',
                                              'ip = os.getenv("ip")',
                                              '',
                                              'aiogram_redis = {',
                                              '    "host": ip',
                                              '}',
                                              '',
                                              'redis = {',
                                              "    'address': (ip, 6379),",
                                              "    'encoding': 'utf8'",
                                              '}'
                                              ]},
                          {'filters/__init__.py': [
                              'from aiogram import Dispatcher',
                              '',
                              'def setup(dp: Dispatcher):',
                              '    pass'
                          ]},
                          {'handlers/__init__.py': [
                              'from .errors import dp',
                              'from .users import dp',
                              '',
                              '__all__ = ["dp"]'
                          ]},
                          'handlers/channels/__init__.py',
                          {'handlers/errors/__init__.py': [
                              'from .error_handler import dp',
                              '',
                              '__all__ = ["dp"]'
                          ]},

                          {"handlers/errors/error_handler.py": [
                              'import logging',
                              '',
                              'from loader import dp',
                              '',
                              '@dp.errors_handler()',
                              'async def errors_handler(update, exception):',
                              '    """',
                              '    Exceptions handler. Catches all exceptions within task factory tasks.',
                              '    :param update:',
                              '    :param exception:',
                              '    :return: stdout logging',
                              '    """',
                              '    from aiogram.utils.exceptions import (Unauthorized, InvalidQueryID, TelegramAPIError,',
                              '                                          CantDemoteChatCreator, MessageNotModified, MessageToDeleteNotFound,',
                              '                                          MessageTextIsEmpty, RetryAfter,',
                              '                                          CantParseEntities, MessageCantBeDeleted, BadRequest)',
                              '    if isinstance(exception, CantDemoteChatCreator):',
                              '        logging.debug("Cant demote chat creator")',
                              '        return True',
                              '',
                              '    if isinstance(exception, MessageNotModified):',
                              "        logging.debug('Message is not modified')",
                              '        return True',
                              '    if isinstance(exception, MessageCantBeDeleted):',
                              "        logging.debug('Message cant be deleted')",
                              '        return True',
                              '    if isinstance(exception, MessageToDeleteNotFound):',
                              "        logging.debug('Message to delete not found')",
                              '        return True',
                              '    if isinstance(exception, MessageTextIsEmpty):',
                              "        logging.debug('MessageTextIsEmpty')",
                              '        return True',
                              '    if isinstance(exception, Unauthorized):',
                              "        logging.info(f'Unauthorized: {exception}')",
                              '        return True',
                              '    if isinstance(exception, InvalidQueryID):',
                              "        logging.exception(f'InvalidQueryID: {exception} Update: {update}')",
                              '        return True',
                              '    if isinstance(exception, TelegramAPIError):',
                              "        logging.exception(f'TelegramAPIError: {exception} Update: {update}')",
                              '        return True',
                              '    if isinstance(exception, RetryAfter):',
                              "        logging.exception(f'RetryAfter: {exception} Update: {update}')",
                              '        return True',
                              '    if isinstance(exception, CantParseEntities):',
                              "        logging.exception(f'CantParseEntities: {exception} Update: {update}')",
                              '        return True',
                              '    if isinstance(exception, BadRequest):',
                              "        logging.exception(f'CantParseEntities: {exception} Update: {update}')",
                              '        return True',
                              "    logging.exception(f'Update: {update} {exception}')"
                          ]},
                          'handlers/groups/__init__.py',
                          {'handlers/users/__init__.py': [
                              'from .help import dp',
                              'from .start import dp',
                              'from .echo import dp',
                              '',
                              '__all__ = ["dp"]'
                          ]},
                          {'handlers/users/echo.py': [
                              'from aiogram import types',
                              'from loader import dp',
                              '',
                              '@dp.message_handler()',
                              'async def bot_echo(message: types.Message):',
                              '    await message.answer(message.text)'
                          ]},
                          {'handlers/users/help.py': [
                              'from aiogram import types',
                              'from aiogram.dispatcher.filters.builtin import CommandHelp',
                              '',
                              'from loader import dp',
                              'from utils.misc import rate_limit',
                              '',
                              "@rate_limit(5, 'help')",
                              '@dp.message_handler(CommandHelp())',
                              'async def bot_help(message: types.Message):',
                              '    text = [',
                              "        'Список команд: ',",
                              "        '/start - Начать диалог',",
                              "        '/help - Получить справку'",
                              '    ]',
                              "    await message.answer(' '.join(text))"
                          ]},
                          {'handlers/users/start.py': [
                              'from aiogram import types',
                              'from aiogram.dispatcher.filters.builtin import CommandStart',
                              '',
                              'from loader import dp',
                              '',
                              '@dp.message_handler(CommandStart())',
                              'async def bot_start(message: types.Message):',
                              "    await message.answer(f'Привет, {message.from_user.full_name}!')"
                          ]},
                          {'app.py': [
                              "from utils.set_bot_commands import set_default_commands",
                              '',
                              'async def on_startup(dp):',
                              '    import filters',
                              '    import middlewares',
                              '    filters.setup(dp)',
                              '    middlewares.setup(dp)',
                              '',
                              '    from utils.notify_admins import on_startup_notify',
                              '    await on_startup_notify(dp)',
                              '    await set_default_commands(dp)',
                              '',
                              "if __name__ == '__main__':",
                              '    from aiogram import executor',
                              '    from handlers import dp',
                              '',
                              '    executor.start_polling(dp, on_startup=on_startup)'
                          ]},
                          {'loader.py': [
                              'from aiogram import Bot, Dispatcher, types',
                              'from aiogram.contrib.fsm_storage.memory import MemoryStorage',
                              '',
                              'from data import config',
                              'bot = Bot(token=config.BOT_TOKEN, parse_mode=types.ParseMode.HTML)',
                              'storage = MemoryStorage()',
                              'dp = Dispatcher(bot, storage=storage)'
                          ]},
                          'keyboards/__init__.py',
                          'keyboards/default/__init__.py',
                          'keyboards/inline/__init__.py',
                          {'middlewares/__init__.py': [
                              'from aiogram import Dispatcher',
                              '',
                              'from .throttling import ThrottlingMiddleware',
                              '',
                              'def setup(dp: Dispatcher):',
                              '    dp.middleware.setup(ThrottlingMiddleware())'
                          ]},
                          {'middlewares/throttling.py': [
                              'import asyncio',
                              '',
                              'from aiogram import types, Dispatcher',
                              'from aiogram.dispatcher import DEFAULT_RATE_LIMIT',
                              'from aiogram.dispatcher.handler import CancelHandler, current_handler',
                              'from aiogram.dispatcher.middlewares import BaseMiddleware',
                              'from aiogram.utils.exceptions import Throttled',
                              '',
                              'class ThrottlingMiddleware(BaseMiddleware):',
                              '    """',
                              '    Simple middleware',
                              '    """',
                              '',
                              "    def __init__(self, limit=DEFAULT_RATE_LIMIT, key_prefix='antiflood_'):",
                              '        self.rate_limit = limit',
                              '        self.prefix = key_prefix',
                              '        super(ThrottlingMiddleware, self).__init__()',
                              '    async def on_process_message(self, message: types.Message, data: dict):',
                              '        handler = current_handler.get()',
                              '        dispatcher = Dispatcher.get_current()',
                              '        if handler:',
                              "            limit = getattr(handler, 'throttling_rate_limit', self.rate_limit)",
                              '            key = getattr(handler, "throttling_key", f"{self.prefix}_{handler.__name__}")',
                              '        else:',
                              '            limit = self.rate_limit',
                              '            key = f"{self.prefix}_message"',
                              '        try:',
                              '            await dispatcher.throttle(key, rate=limit)',
                              '        except Throttled as t:',
                              '            await self.message_throttled(message, t)',
                              '            raise CancelHandler()',
                              '',
                              '    async def message_throttled(self, message: types.Message, throttled: Throttled):',
                              '        handler = current_handler.get()',
                              '        dispatcher = Dispatcher.get_current()',
                              '        if handler:',
                              '            key = getattr(handler, "throttling_key", f"{self.prefix}_{handler.__name__}")',
                              '        else:',
                              '            key = f"{self.prefix}_message"',
                              '        delta = throttled.rate - throttled.delta',
                              '        if throttled.exceeded_count <= 2:',
                              "            await message.reply('Too many requests! ')",
                              '        await asyncio.sleep(delta)',
                              '        thr = await dispatcher.check_key(key)',
                              '        if thr.exceeded_count == throttled.exceeded_count:',
                              "            await message.reply('Unlocked.')"
                          ]},
                          'states/__init__.py',
                          'utils/__init__.py',

                          {'utils/notify_admins.py': [
                              'import logging',
                              '',
                              'from aiogram import Dispatcher',
                              '',
                              'from data.config import admins',
                              '',
                              'async def on_startup_notify(dp: Dispatcher):',
                              '    for admin in admins:',
                              '        try:',
                              '            await dp.bot.send_message(admin, "Бот Запущен и готов к работе")',
                              '',
                              '        except Exception as err:',
                              '            logging.exception(err)'
                          ]},
                          {'utils/set_bot_commands.py': [
                              'from aiogram import types',
                              '',
                              'async def set_default_commands(dp):',
                              '    await dp.bot.set_my_commands([',
                              '        types.BotCommand("start", "Запустить бота"),',
                              '        types.BotCommand("help", "Помощь"),',
                              '    ])'
                          ]},
                          {'requirements.txt': [
                              'aiogram>=2.0',
                              'aiohttp>=3.0',
                              'python-dotenv'
                          ]}
                          ]

    class contrib(object):
        TELEGRAM_FILES = []


if __name__ == '__main__':
    constructor = Templates()
    constructor.telegram_bot_template()
