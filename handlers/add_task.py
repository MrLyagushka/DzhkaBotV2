from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message

from keyboards.add_task import keyboard_add_task
from keyboards.choose_a_number_of_task import keyboard_list_a_number_of_task
from handlers.global_menu import GlobalMenu

router_add_task = Router()

class AddTask(StatesGroup):
    first = State()
    second = State()
    third = State()


@router_add_task.message(GlobalMenu.teacher)
async def add_task1(message: Message, state: FSMContext):
    await state.clear()
    await state.set_state(AddTask.first)
    await message.answer('Выберите источник заданий', reply_markup=keyboard_add_task.markup)

@router_add_task.message(AddTask.first)
async def add_task2(message: Message, state: FSMContext):
    await state.update_data(choice1=message.text)
    await message.answer('Выберите номер задания', reply_markup=keyboard_list_a_number_of_task.markup)
    await state.set_state(AddTask.second)

@router_add_task.message(AddTask.second)
async def add_task3(message: Message, state: FSMContext):
    await state.update_data(choice2=message.text)
    choice1 = (await state.get_data())['choice1']
    choice2 = (await state.get_data())['choice2']
    print(choice1)
    print(choice2)
