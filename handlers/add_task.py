from aiogram import Router, F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery

from keyboards.add_task import keyboard_add_task, keyboard_add_task2
from keyboards.choose_a_number_of_task import keyboard_list_a_number_of_task
from handlers.global_menu import GlobalMenu
from utils.template import DinamicKeyboard
from keyboards.global_menu import global_menu_teacher
from utils.task_bank import TaskBank
from utils.task import Task
from utils.users import Teacher


router_add_task = Router()

class AddTask(StatesGroup):
    first = State()
    second = State()
    third = State()
    fourth = State()
    fifth = State()


@router_add_task.message(GlobalMenu.teacher, F.text == "Добавить тест")
async def add_task1(message: Message, state: FSMContext):
    #Реализуем проверку на наличие учеников

    teacher = Teacher()
    teacher.get_statistics(message.from_user.id)
    number_of_student = teacher.number_of_students
    if number_of_student == 0:
        await message.answer("У вас нет учеников, сначала добавьте минимум одного ученика, что бы разблокировать это меню", reply_markup=global_menu_teacher.markup)
        await state.set_state(GlobalMenu.teacher)
    else:
        await state.clear()
        await message.answer("Выберите ученика", reply_markup=DinamicKeyboard(1,3,'no',0,f'st_{message.chat.id}').generate_keyboard())
        await state.set_state(AddTask.first)


@router_add_task.callback_query(F.data[:13] == "callback_data", AddTask.first)
async def add_task2(callback: CallbackQuery, state: FSMContext):
    await state.update_data(user_id=callback.data)
    await callback.answer()
    await callback.message.answer('Выберите источник заданий', reply_markup=keyboard_add_task.markup)
    await state.set_state(AddTask.second)


@router_add_task.message(F.text == "Выдать ученику еще одну задачу", AddTask.fifth)
async def add_task21(message: Message, state: FSMContext):
    await message.answer('Выберите источник заданий', reply_markup=keyboard_add_task.markup)
    await state.set_state(AddTask.second)


@router_add_task.message(AddTask.second)
async def add_task3(message: Message, state: FSMContext):
    await state.update_data(task_source=message.text)
    task_source = (await state.get_data())['task_source']
    user_id = (await state.get_data())['user_id'].split('_')[3]

    if task_source == 'Банк заданий':
        await message.answer('Выберите номер задания', reply_markup=keyboard_list_a_number_of_task.markup)
        await state.set_state(AddTask.third)
    if task_source == "Добавить задание":
        await message.answer("Тут будут шаблоны для ввода своих заданий", reply_markup=global_menu_teacher.markup)
        await state.set_state(GlobalMenu.teacher)
        
@router_add_task.message(AddTask.third)
async def add_task4(message: Message, state: FSMContext):
    await state.update_data(task_number=message.text)
    task_number = (await state.get_data())['task_number'].split('№')[1]
    user_id = (await state.get_data())['user_id'].split('_')[3]

    button_list = TaskBank().get_task(number=int(task_number))

    if len(button_list) == 0:
        await message.answer("Тут пока пусто", reply_markup=global_menu_teacher.markup)
        await state.set_state(GlobalMenu.teacher)
    else:
        await message.answer('Выберите задание для отправки', reply_markup=DinamicKeyboard(1, 3, 'no', 0, f'tt_{task_number}').generate_keyboard())
        await state.set_state(AddTask.fourth)


@router_add_task.callback_query(F.data[:13] == "callback_data", AddTask.fourth)
async def add_task5(callback: CallbackQuery, state: FSMContext, bot: Bot):
    task_number = (await state.get_data())['task_number'].split('№')[1]
    user_id = (await state.get_data())['user_id'].split('_')[3]

    await callback.answer()

    task = (TaskBank().get_task_with_id(task_number, callback.data.split('_')[3]))[0]
    new_task = Task().new_task(id_teacher=callback.message.chat.id, id_student=int(user_id), id_task=task[3], text=task[6])
    
    await bot.send_message(chat_id=int(user_id), text='Привет, тебе пришло новое задание!')
    await callback.message.answer('Выбери действие', reply_markup=keyboard_add_task2.markup)
    await state.set_state(AddTask.fifth)


# @router_add_task.callback_query(F.data[:13] == "callback_data", AddTask.fourth)
# async def add_task5(callback: CallbackQuery, state: FSMContext, bot: Bot):
#     choice2 = (await state.get_data())['choice2'].split('№')[1]
#     choice3 = (await state.get_data())['choice3'].split('_')[3]
#     await callback.answer()
#     task = (TaskBank().get_task_with_id(choice2, choice3))[0]
#     new_task = Task().new_task(id_teacher=callback.message.chat.id, id_student=int(callback.data.split('_')[3]), id_task=task[3], text=task[6])
    
#     await bot.send_message(chat_id=int(callback.data.split('_')[3]), text='Привет, тебе пришло новое задание!')
#     await callback.message.answer('Выбери действие', reply_markup=global_menu_teacher.markup)
#     await state.set_state(GlobalMenu.teacher)


# @router_add_task.message(AddTask.first)
# async def add_task2(message: Message, state: FSMContext):
#     await state.update_data(choice1=message.text)
#     await message.answer('Выберите номер задания', reply_markup=keyboard_list_a_number_of_task.markup)
#     await state.set_state(AddTask.second)

# @router_add_task.message(AddTask.second)
# async def add_task3(message: Message, state: FSMContext):
#     await state.update_data(choice2=message.text)
#     choice1 = (await state.get_data())['choice1']
#     choice2 = (await state.get_data())['choice2'].split('№')[1]

#     button_list = TaskBank().get_task(number=int(choice2))

#     if choice1 == 'Банк заданий':
#         if len(button_list) == 0:
#             await message.answer("Тут пока пусто", reply_markup=global_menu_teacher.markup)
#             await state.set_state(GlobalMenu.teacher)
#         else:
#             await message.answer('Выберите задание для отправки', reply_markup=DinamicKeyboard(1, 3, 'no', 0, f'tt_{choice2}').generate_keyboard())
#             await state.set_state(AddTask.third)
#     if choice1 == "Добавить задание":
#         await message.answer("Тут будут шаблоны для ввода своих заданий", reply_markup=global_menu_teacher.markup)
#         await state.set_state(GlobalMenu.teacher)


# @router_add_task.callback_query(F.data[:13] == "callback_data", AddTask.third)
# async def add_task4(callback: CallbackQuery, state: FSMContext):
#     await state.update_data(choice3=callback.data)
#     await callback.answer()
#     # await callback.message.answer("Выберите ученика", reply_markup=DinamicKeyboard(1,3,'no',0,f'st_{callback.message.chat.id}').generate_keyboard())
#     await state.set_state(AddTask.fourth)



    
