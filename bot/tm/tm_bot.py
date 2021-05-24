""""""

"""База данных и компоненты для работы с ней"""
from engine.db_manager import DbManager
from data.config import DB_PATH
DB = DbManager(DB_PATH)

"""XML и компоненты для работы с ним"""
from engine.xml_manager import XmlTreeManager
from data.config import XML_PATH
XML = XmlTreeManager(XML_PATH)

"""Основные элементы aiogram для работы бота"""
import logging
from aiogram import Bot, Dispatcher, executor, types

config = DB.get_config('tm')
TM_BOT_TOKEN = config['token']
is_on = config['is_on']
messenger_id = config['messenger_id']

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
    @param message сообщение от пользователя
    @param DB база данных пользователей
    """
    config = DB.get_config('tm')
    a = answer_generator.generate(config['is_on'], DB, XML, messenger_id, message.from_user.id, message.text)
    await message.answer(a['message'], reply_markup=kb.get_keyboard_markup(a['button_text_list']))

"""Запускаем бота"""
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)