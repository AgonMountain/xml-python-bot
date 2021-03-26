import logging
from aiogram import Bot, Dispatcher, executor, types
from data.config import TM_DB, XML, TM_BOT_TOKEN, IDONTUNDERSTAND
from bot.tm.tm_keyboard import TmKeyboard


logging.basicConfig(level=logging.INFO)
bot = Bot(token=TM_BOT_TOKEN)
dp = Dispatcher(bot)
kb = TmKeyboard()


@dp.message_handler()
async def bot(message: types.Message):

    user_id = message.from_user.id

    if TM_DB.get_current_element_id(user_id) == None:
        TM_DB.add(user_id)

    element = XML.get_element_by_id(TM_DB.get_current_element_id(user_id))

    ms = element.text.text

    transition_list = element.transition_list
    addition_list = element.addition_list

    understand_flag = False

    for transition in transition_list:
        if message.text == transition.text:
            understand_flag = True
            next_element_id = transition.get('next_element_id')
            TM_DB.update_current_element_id(user_id, next_element_id)

            element = XML.get_element_by_id(next_element_id)
            ms = XML.get_element_by_id(next_element_id).text.text
            transition_list = element.transition_list
            addition_list = element.addition_list
            break

    if not understand_flag:
        for addition in addition_list:
            if message.text == addition.text:
                understand_flag = True
                element_id = addition.get('element_id')
                ms = XML.get_element_by_id(element_id).text.text
                break

    if not understand_flag and element.id != '-1':
        ms = IDONTUNDERSTAND

    transition_text_list = [transition.text for transition in transition_list]
    addition_text_list = [addition.text for addition in addition_list]

    await message.answer(ms, reply_markup=kb.get_keyboard_markup(transition_text_list + addition_text_list))


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)