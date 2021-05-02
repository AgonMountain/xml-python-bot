import logging
from aiogram import Bot, Dispatcher, executor, types
from data.config import TM_DB, XML, TM_BOT_TOKEN
from bot.tm.tm_keyboard import TmKeyboard
from bot import answer_generator

"""Основные элементы aiogram для работы бота"""
logging.basicConfig(level=logging.INFO)
bot = Bot(token=TM_BOT_TOKEN)
dp = Dispatcher(bot)
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