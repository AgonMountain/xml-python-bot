import json


class VkKeyboard(object):

    def get_keyboard_markup(self, button_text_list):
        """Получить клавиатуру с N кнопками"""

        buttons_text = []
        for button_text in button_text_list:
            buttons_text += [[self.get_button(button_text, 'secondary')]]


        keyboard = {
            "one_time": False,
            "buttons": buttons_text

        }

        keyboard = json.dumps(keyboard, ensure_ascii=False).encode('utf-8')
        return str(keyboard.decode('utf-8'))

    def get_button(self, text, color):
        return {
            "action": {
                "type": "text",
                "payload": "{\"button\": \"" + "1" + "\"}",
                "label": f"{text}"
            },
            "color": f"{color}"
        }

    def get_button_list(self, button_text_list):
        arr = [VkKeyboard.get_button(button_text_list[i], 'positive') for i in range(len(button_text_list))]
        return arr