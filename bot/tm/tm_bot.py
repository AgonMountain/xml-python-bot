""""""

"""База данных и компоненты для работы с ней"""
import os.path
from engine.db_module.db_manager import DbManager
from data.config import DB_PATH, DB_TELEGRAM_TABLE_NAME
TM_DB = DbManager(os.path.abspath(os.path.join(DB_PATH)), DB_TELEGRAM_TABLE_NAME)

"""XML и компоненты для работы с ним"""
from engine.xml_module.xml_manager import XmlTreeManager
from data.config import XML_PATH
XML = XmlTreeManager(XML_PATH)

"""Основные элементы aiogram для работы бота"""
import logging
from aiogram import Bot, Dispatcher, executor, types
from data.config import TM_BOT_TOKEN
logging.basicConfig(level=logging.INFO)
bot = Bot(token=TM_BOT_TOKEN)
dp = Dispatcher(bot)

"""Клавиатура и генератор ответов для бота"""
from bot.tm.tm_keyboard import TmKeyboard
from bot import answer_generator
kb = TmKeyboard()


@dp.message_handler()
async def bot(message: types.Message):
    """
    Отловливать сообщения от пользователя и отправлять сообщения в ответ
    > message сообщение от пользователя
    > TM_DB база данных пользователей
    """
    a = answer_generator.generate(TM_DB, XML, message.from_user.id, message.text)
    await message.answer(a['message'], reply_markup=kb.get_keyboard_markup(a['button_text_list']))

"""Запускаем бота"""
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)