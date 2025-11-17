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
        st_idteacher или ts_idstudent или tt_number
        """
        self.first_index = first_index
        self.row = row
        self.column = column
        self.is_always_bigger_column_multiply_row = is_always_bigger_column_multiply_row
        self.button_info = button_info

    def generate_keyboard(self):
        """
        На будущее, тут можно вырать из трех режимов, так легче, чем указывать путь к файлу,
          или что-то подобноею После выбора режима и ввода через :  id , """
        dinamic_keyboard = Menu('inline', self.row+1)

        if self.button_info.split('_')[0] == 'st':
            st = Teacher()
            st.get_statistics(int(self.button_info.split('_')[1]))
            self.button_list = st.students_id
        elif self.button_info.split('_')[0] == 'ts':
            ts = Task()
            ts.get_task(int(self.button_info.split('_')[1]))
            self.button_list = ts.task_student
        elif self.button_info.split('_')[0] == 'tt':
            self.button_list = TaskBank().get_task(int(self.button_info.split('_')[1]))
        count = 0
        while count < self.row * self.column and self.first_index + count < len(self.button_list):
            row = count // self.column
            if self.button_info.split('_')[0] == 'st':
                dinamic_keyboard.new_button(row_number=row+1, text=str(self.button_list[self.first_index+count]),# Т.к. в классе Menu, row_number идет от 0, для удобства пользования
                                        callback_data=f'callback_data_{self.button_info.split("_")[0]}_{self.button_list[self.first_index+count]}')
            elif self.button_info.split('_')[0] == 'ts':
                dinamic_keyboard.new_button(row_number=row+1, text=str(self.button_list[self.first_index+count][2]),# Т.к. в классе Menu, row_number идет от 0, для удобства пользования
                                        callback_data=f'callback_data_{self.button_info.split("_")[0]}_{self.button_list[self.first_index+count][3]}')
            elif self.button_info.split('_')[0] == 'tt':
                dinamic_keyboard.new_button(row_number=row+1, text=str(self.button_list[self.first_index+count][3]),# Т.к. в классе Menu, row_number идет от 0, для удобства пользования
                                            callback_data=f'callback_data_{self.button_info.split("_")[0]}_{self.button_list[self.first_index+count][3]}')
            count += 1
        if count == self.row*self.column:
            dinamic_keyboard.new_button(row_number=self.row+1, text='<', # Т.к. в классе Menu, row_number идет от 0, для удобства пользования
                                    callback_data=MyCallbackData(callback_data='<', first_index=self.first_index, row=self.row, column=self.column, is_always_bigger=self.is_always_bigger_column_multiply_row, button_info=self.button_info, len_button_list=len(self.button_list)).pack())
            dinamic_keyboard.new_button(row_number=self.row+1, text='>', callback_data=MyCallbackData(callback_data='>', first_index=self.first_index, row=self.row, column=self.column, is_always_bigger= self.is_always_bigger_column_multiply_row, button_info=self.button_info, len_button_list=len(self.button_list)).pack())
        return dinamic_keyboard.markup