import logging

from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery

from keyboards.choose_a_number_of_task import keyboard_list_a_number_of_task
from filters.is_teacher import IsTeacher
from keyboards.task_bank import choose_next_step
from handlers.global_menu import GlobalMenu

router_task_bank = Router()

class NumberTask(StatesGroup):
    first = State()
    second = State()

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
    await state.set_state(GlobalMenu.teacher)