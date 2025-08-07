from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton, KeyboardButton
from typing_extensions import Literal


class Menu:
    def __init__(self, type: Literal['inline', 'reply'], row, one_time_keyboard=False):
        """
        В данном конструкторе вводится тип кнопок для клавиатуры и количество строк. Добавлять кнопки в ряды можно до 5-6
        One_time_keyboard - одно использование
        :param type:
        :param row:
        """
        self.type = type
        self.keyboard = [[] for _ in range(row)]
        self.one_time_keyboard=one_time_keyboard
        if type == 'reply':
            self.markup = ReplyKeyboardMarkup(keyboard=self.keyboard, resize_keyboard=True, one_time_keyboard=self.one_time_keyboard)
        elif type == 'inline':
            self.markup = InlineKeyboardMarkup(inline_keyboard=self.keyboard)

    def new_button(self, text: str, row_number: int, url=None, callback_data=None):
        """
        Вводится номер строки в которую вставляется кнопка и текст кнопки. Если клавиатура типа inline, то вводится еще и callback и/или url
        :return:
        """
        if self.type == 'reply':
            self.keyboard[row_number-1].append(KeyboardButton(text=text)) # -1 т к это индекс
            self.markup = ReplyKeyboardMarkup(keyboard=self.keyboard, resize_keyboard=True, one_time_keyboard=self.one_time_keyboard)
        elif self.type == 'inline':
            self.keyboard[row_number-1].append(InlineKeyboardButton(text=text, url=url, callback_data=callback_data))
            self.markup = InlineKeyboardMarkup(inline_keyboard=self.keyboard)

    def printf(self):
        print(self.markup)
        print(self.keyboard)