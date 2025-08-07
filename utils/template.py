from typing import List
from aiogram.filters.callback_data import CallbackData

from typing_extensions import Literal, TypedDict
from utils.task_bank import TaskBank
from utils.users import Teacher, Student
from utils.task import Task
from utils.menu import Menu




class MyCallbackData(CallbackData, prefix='my'):
    callback_data: str
    first_index: int
    row: int
    column: int
    is_always_bigger: Literal['yes', 'no']
    button_info: str
    len_button_list: int


class DinamicKeyboard():

    def __init__(self, row, column, is_always_bigger_column_multiply_row: Literal['yes', 'no'], first_index,
                 button_info: str):
        """
        Кароч, указываешь количество строк - row, столбцов - column. Также введи, будет ли твоя клавиатура
        всегда больше чем column*row или нет. И еще список кнопок.
        Формат button_info: st, ts, tt. Список учеников, список заданий у ученика, список заданий у учителя.
        st:id_teacher или ts:id_student или tt:number
        :param column:
        :param row:
        """
        self.first_index = first_index
        self.row = row
        self.column = column
        self.is_always_bigger_column_multiply_row = is_always_bigger_column_multiply_row
        self.button_info = button_info

    def generate_keyboard(self):
        dinamic_keyboard = Menu('inline', self.row+1)

        if self.button_info.split(':')[0] == 'st':
            self.button_list = Teacher().get_statistics(int(self.button_info.split(':')[1])).students_id
        elif self.button_info.split(':')[0] == 'ts':
            self.button_list = Task().get_task(int(self.button_info.split(':')[1])).task_student
        elif self.button_info.split(':')[0] == 'tt':
            self.button_list = TaskBank().get_task(number=int(self.button_info.split(':')[1])).number

        count = self.first_index
        while count < self.row * self.column:
            row = count // self.column
            dinamic_keyboard.new_button(row_number=row+1, text=self.button_list[count]['text'],# Т.к. в классе Menu, row_number идет от 0, для удобства пользования
                                        callback_data=self.button_list[count]['callback_data'])
            count += 1
        dinamic_keyboard.new_button(row_number=self.row+1, text='<', # Т.к. в классе Menu, row_number идет от 0, для удобства пользования
                                    callback_data=MyCallbackData(callback_data='<', first_index=self.first_index, row=self.row, column=self.column, is_always_bigger=self.is_always_bigger_column_multiply_row, button_info=self.button_info, len_button_list=len(self.button_list)).pack())
        dinamic_keyboard.new_button(row_number=self.row+1, text='>', callback_data=MyCallbackData(callback_data='>', first_index=self.first_index, row=self.row, column=self.column, is_always_bigger= self.is_always_bigger_column_multiply_row, button_info=self.button_info, len_button_list=len(self.button_list)).pack())
        return dinamic_keyboard.markup