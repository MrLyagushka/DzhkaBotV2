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
    number = State()

@router_task_bank.message(GlobalMenu.teacher)
async def task_bank(message: Message, state: FSMContext):
    await message.answer('Это банк заданий для ЕГЭ по русскому языку. В него можно добавлять задания по определенным шаблонам', reply_markup=keyboard_list_a_number_of_task.markup)
    await state.set_state(NumberTask.number)

@router_task_bank.message(NumberTask.number)
async def choose_number_task(message: Message, state: FSMContext):
    await state.update_data(number=message.text)
    number = (await state.get_data())['number'].split('№')[1]
    await message.answer('Выберите действие', reply_markup=choose_next_step(number))
    await state.set_state(NumberTask.first)

@router_task_bank.callback_query(NumberTask.first)
async def see(callback: CallbackQuery, state: FSMContext):
    number = callback.data.split(':')[1]
    try:
        number = int(number)
    except Exception as e:
        logging.info(f'Ошибка в функции see: {e}')
        await callback.message.answer(f'Ошибка, передайте этот текст в тех. поддержку: {e}')
