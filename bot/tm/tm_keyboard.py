from aiogram.types import \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton


class TmKeyboard(object):

    def get_keyboard_markup(self, button_text_list):
        """Получить клавиатуру с N кнопками"""
        if len(button_text_list) > 0:
            rkm = ReplyKeyboardMarkup(resize_keyboard=True)
            for i in range(len(button_text_list)):
                rkm.add(KeyboardButton(button_text_list[i]))
            return rkm

    def get_inline_keyboard_markup(self, button_text_list, callback_data_list):
        """Получить клавиатуру с N inline кнопками"""
        if len(button_text_list) == len(callback_data_list) and len(button_text_list) > 0:
            ikm = InlineKeyboardMarkup()
            for i in range(len(button_text_list)):
                ikm.add(InlineKeyboardButton(button_text_list[i], callback_data=callback_data_list[i]))
            return ikm