# Тут я хочу описать создание любых шаблонов для ввода их репетитором. Использовать буду классы
# Еще тут будет класс динамических клавиатур
from typing import List
from aiogram.filters.callback_data import CallbackData

from typing_extensions import Literal, TypedDict
from utils.menu import Menu


class DictChildrenInfo(TypedDict):
    text: str
    callback_data: str

class MyCallbackData(CallbackData, prefix='my'):
    callback_data: str
    first_index: int
    row: int
    column: int
    is_always_bigger: Literal['yes', 'no']

# class DictInfo(TypedDict):
#     callback_data: str
#     first_index: int
#     row: int
#     column: int
#     is_always_bigger_column_multiply_row: Literal['yes', 'no']
#     button_list: List[DictChildrenInfo]

class DinamicKeyboard():

    def __init__(self, row, column, is_always_bigger_column_multiply_row: Literal['yes', 'no'], first_index,
                 button_list: List[DictChildrenInfo]):
        """
        Кароч, указываешь количество строк - row, столбцов - column. Также введи, будет ли твоя клавиатура
        всегда больше чем column*row или нет. И еще список кнопок.
        Формат button_list: [{'text': 'text', 'callback_data': 'callback_data'},{...}, ...]
        :param column:
        :param row:
        """
        self.first_index = first_index
        self.row = row
        self.column = column
        self.is_always_bigger_column_multiply_row = is_always_bigger_column_multiply_row
        self.button_list = button_list

    def generate_keyboard(self):
        dinamic_keyboard = Menu('inline', self.row+1)

        count = self.first_index
        while count < self.row * self.column:
            print(count, 'count')
            row = count // self.column
            print(row, 'row')
            dinamic_keyboard.new_button(row_number=row+1, text=self.button_list[count]['text'],# Т.к. в классе Menu, row_number идет от 0, для удобства пользования
                                        callback_data=self.button_list[count]['callback_data'])
            count += 1
        print(self.row+1)
        dinamic_keyboard.new_button(row_number=self.row+1, text='<', # Т.к. в классе Menu, row_number идет от 0, для удобства пользования
                                    callback_data=MyCallbackData(callback_data='<', first_index=self.first_index, row=self.row, column=self.column, is_always_bigger= self.is_always_bigger_column_multiply_row).pack())
        dinamic_keyboard.new_button(row_number=self.row+1, text='>', callback_data=MyCallbackData(callback_data='>', first_index=self.first_index, row=self.row, column=self.column, is_always_bigger= self.is_always_bigger_column_multiply_row).pack())
        return dinamic_keyboard.markup


# dinkeyb = DinamicKeyboard(1, 2, 'yes', 0, [{'text': 'abs', 'callback_data': 'abss'},
#                                            {'text': 'abs', 'callback_data': 'abss'},
#                                            {'text': 'abs', 'callback_data': 'abss'}])
# for i in dinkeyb.generate_keyboard():
#     for j in i:
#         for k in j:
#             print(k)