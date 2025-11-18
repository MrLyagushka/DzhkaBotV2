from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext


from handlers.global_menu import GlobalMenu
from utils.task import Task
from utils.template import DinamicKeyboard
from utils.task_bank import TaskBank
from handlers.global_menu import global_menu_student

router_do_test = Router()

class DoTest(StatesGroup):
    first = State()
    second = State()
    third = State()
    fourth = State()

@router_do_test.message(F.text == "Решать тесты")
async def do_test1(message: Message, state: FSMContext):
    task = Task()
    task.get_task(id_student=message.from_user.id)
    task_student = task.task_student

    await message.answer("Выберите задание: ", reply_markup=DinamicKeyboard(1,3,'no',0,f'ts_{message.from_user.id}').generate_keyboard())
    await state.set_state(DoTest.first)

@router_do_test.callback_query(F.data[:13] == "callback_data", DoTest.first)
async def do_test2(callback: CallbackQuery, state: FSMContext):
    await callback.answer()

    await state.set_state(DoTest.second)
    await state.update_data(choice1=callback.data)
    print(callback.data)
     
    choice1 = int((await state.get_data())['choice1'].split('_')[3])
    print(choice1)
    task = Task()
    task.get_task(id_student=callback.message.chat.id)
    task_student = task.task_student



    await callback.message.answer(task_student[choice1][4]+"\n\nВведите правильный ответ ниже:\nЕсли ответом являются несколько цифр - укажите их через пробел\nЕсли ответом являются несколько слов - укажите их через пробел\nЕсли ответом является фраза - перепишите её заглавными буквами.")

@router_do_test.message(DoTest.second)
async def do_test3(message: Message, state: FSMContext):
    await state.update_data(answer=message.text)
    answer = (await state.get_data())['answer']
    choice1 = int((await state.get_data())['choice1'].split('_')[3])
    print(answer)
    print(choice1)

    task = Task()
    task.get_task(id_student=message.from_user.id)
    task_student = task.task_student

    correct_answer = task_student[choice1]
    print(correct_answer)
    return
    if message.text.strip().lower() == correct_answer.strip().lower():
        await message.answer("Правильный ответ! 🎉", reply_markup=global_menu_student.markup)
    else:
        await message.answer(f"Неправильный ответ. ❌\nПравильный ответ: {correct_answer}", reply_markup=global_menu_student.markup)

    await state.clear()
    await state.set_state(GlobalMenu.student)