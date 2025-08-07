from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from keyboards.global_menu import global_menu_student, global_menu_first_visit, global_menu_teacher
from filters.is_student import IsStudent
from filters.is_teacher import IsTeacher
from utils.new_teacher import NewTeacher
from utils.new_student import NewStudent

router_command_start = Router()

class GlobalMenu(StatesGroup):
    teacher = State()
    student = State()
    third = State()


@router_command_start.message(CommandStart(), IsTeacher())
async def _start(message: Message, state: FSMContext):
    await state.clear()
    await message.answer('Привет, отличного дня!', reply_markup=global_menu_teacher.markup)
    await state.set_state(GlobalMenu.teacher)


@router_command_start.message(CommandStart(), IsStudent())
async def _start(message: Message, state: FSMContext):
    await state.clear()
    await message.answer('Привет, отличного дня!', reply_markup=global_menu_student.markup)
    await state.set_state(GlobalMenu.student)


@router_command_start.message(CommandStart())
async def _start(message: Message, state: FSMContext):
    await state.clear()
    await message.answer('Привет, я вижу ты первый раз тут, кто ты?', reply_markup=global_menu_first_visit.markup)
    await state.set_state(GlobalMenu.third)

@router_command_start.message(GlobalMenu.third)
async def _new_teacher_or_student(message: Message, state: FSMContext):
    await state.update_data(choice=message.text)
    if (await state.get_data())['choice'] == 'Я учитель':
        if NewTeacher(message.from_user.id).check():
            await message.answer('Вы зарегистрированы как учитель', reply_markup=global_menu_teacher.markup)
        else:
            await message.answer('Вы уже зарегистрированы в системе')
    else:
        if NewStudent(message.from_user.id).check():
            await message.answer('Вы зарегистрированы как ученик', reply_markup=global_menu_student.markup)
        else:
            await message.answer('Вы уже зарегистрированы в системе')
    await state.clear()

@router_command_start.message(F.text == 'На главное меню')
async def _new_student(message: Message, state: FSMContext):
    await state.clear()
    await message.answer('Привет, отличного дня!', reply_markup=global_menu_teacher.markup)
    await state.set_state(GlobalMenu.teacher)
