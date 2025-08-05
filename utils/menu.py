# Тут через классы я буду делать меню. Например главное меню, или профиль.
from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton, KeyboardButton
from typing_extensions import Literal


class Menu:
    def __init__(self, type: Literal['inline', 'reply'], row):
        """
        В данном конструкторе вводится тип кнопок для клавиатуры и количество строк. Добавлять кнопки в ряды можно до 5-6
        :param type:
        :param row:
        """
        self.type = type
        self.keyboard = [[] for _ in range(row)]
        if type == 'reply':
            self.markup = ReplyKeyboardMarkup(keyboard=self.keyboard, resize_keyboard=True)
        elif type == 'inline':
            self.markup = InlineKeyboardMarkup(inline_keyboard=self.keyboard)

    def new_button(self, text: str, row_number: int, url=None, callback_data=None):
        """
        Вводится номер строки в которую вставляется кнопка и текст кнопки. Если клавиатура типа inline, то вводится еще и callback и/или url
        :return:
        """
        if self.type == 'reply':
            self.keyboard[row_number-1].append(KeyboardButton(text=text)) # -1 т к это индекс
            self.markup = ReplyKeyboardMarkup(keyboard=self.keyboard, resize_keyboard=True)
        elif self.type == 'inline':
            self.keyboard[row_number-1].append(InlineKeyboardButton(text=text, url=url, callback_data=callback_data))
            self.markup = InlineKeyboardMarkup(inline_keyboard=self.keyboard)

    def printf(self):
        print(self.markup)
        print(self.keyboard)