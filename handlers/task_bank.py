import logging

from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery

from keyboards.global_menu import global_menu_teacher
from keyboards.choose_a_number_of_task import keyboard_list_a_number_of_task
from filters.is_teacher import IsTeacher
from keyboards.task_bank import choose_next_step
from handlers.global_menu import GlobalMenu
from utils.template import DinamicKeyboard
from utils.task_bank import TaskBank
from utils.users import Teacher, Student

router_task_bank = Router()

class NumberTask(StatesGroup):
    first = State()
    second = State()
    third = State()

@router_task_bank.message(GlobalMenu.teacher and F.text == "Банк заданий")
async def task_bank(message: Message, state: FSMContext):
    await message.answer('Это банк заданий для ЕГЭ по русскому языку. В него можно добавлять задания по определенным шаблонам', reply_markup=choose_next_step.markup)
    await state.set_state(NumberTask.first)

@router_task_bank.message(NumberTask.first)
async def choose_number_task(message: Message, state: FSMContext):
    await state.update_data(choice1=message.text)
    await message.answer('Выберите номер задания', reply_markup=keyboard_list_a_number_of_task.markup)
    await state.set_state(NumberTask.second)

@router_task_bank.message(NumberTask.second)
async def see(message: Message, state: FSMContext):
    await state.update_data(choice2=message.text)
    choice1 = (await state.get_data())['choice1']
    choice2 = (await state.get_data())['choice2'].split('№')[1]
 
    button_list = TaskBank().get_task(number=int(choice2))

    if choice1 == 'Посмотреть задания':
        if len(button_list) == 0:
            await message.answer("Тут пока пусто", reply_markup=global_menu_teacher.markup)
            await state.set_state(GlobalMenu.teacher)
        else:
            await message.answer("Выберите задание", reply_markup=DinamicKeyboard(1,3,'no',0,f'tt_{choice2}').generate_keyboard())

    if choice1 == "Добавить задание":
        await message.answer("Временно эта функция будет отсутствовать..")
    #await state.set_state(GlobalMenu.teacher)
    await state.set_state(NumberTask.third)
    

@router_task_bank.callback_query(F.data[:13] == "callback_data", NumberTask.third)
async def choice_task(callback: CallbackQuery, state: FSMContext):
    #Вывод текста задания
    choice2 = (await state.get_data())['choice2'].split('№')[1]
    
    task = TaskBank().get_task_with_id(choice2, int(callback.data.split('_')[3]))
    await callback.answer()
    await callback.message.answer(task[0][6], reply_markup=global_menu_teacher.markup)
    #Блять, разберись с callback_data, надо понять как передаются данные о задании

    await state.set_state(GlobalMenu.teacher)
