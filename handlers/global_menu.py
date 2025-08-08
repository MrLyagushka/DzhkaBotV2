from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup


from keyboards.global_menu import global_menu_student, global_menu_first_visit, global_menu_teacher, global_menu_choice_class
from filters.is_student import IsStudent
from filters.is_teacher import IsTeacher
from utils.users import Teacher, Student

router_command_start = Router()

class GlobalMenu(StatesGroup):
    teacher = State()
    student = State()
    first = State()
    second = State()
    third = State()
    fourth = State()
    


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
    await state.set_state(GlobalMenu.first)

@router_command_start.message(GlobalMenu.first)
async def _new_teacher_or_student(message: Message, state: FSMContext):
    await state.update_data(choice=message.text)
    if (await state.get_data())['choice'] == 'Я учитель':
        teacher = Teacher()
        teacher.new_teacher(message.from_user.id)
        if teacher.check():
            await message.answer('Введите ваше имя и фамилию, например Варя Черноус', reply_markup=ReplyKeyboardRemove())
            await state.set_state(GlobalMenu.second)
        else:
            await message.answer('Вы уже зарегистрированы в системе', reply_markup=global_menu_teacher.markup)
            await state.set_state(GlobalMenu.teacher)
    else:
        student = Student()
        if student.new_student(message.from_user.id).check():
            await message.answer('Введите ваше имя и фамилию, например Варя Черноус', reply_markup=ReplyKeyboardRemove())
            await state.set_state(GlobalMenu.second)
        else:
            await message.answer('Вы уже зарегистрированы в системе', reply_markup=global_menu_student.markup)
            await state.set_state(GlobalMenu.student)

@router_command_start.message(GlobalMenu.second)
async def set_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    name = (await state.get_data())['name']
    choice = (await state.get_data())['choice']
    if choice == 'Я учитель':
        Teacher().set('str', 'name', name, message.from_user.id)
        await message.answer('Вы зарегистрированы как учитель', reply_markup=global_menu_teacher.markup)
        await state.set_state(GlobalMenu.teacher)
    elif choice == 'Я ученик':
        Student().set('str', 'name', name, message.from_user.id)
        await message.answer('В каком ты классе?', reply_markup=global_menu_choice_class.markup)
        await state.set_state(GlobalMenu.third)

@router_command_start.message(GlobalMenu.third)
async def set_class(message: Message, state: FSMContext):
    await state.update_data(class_number=message.text)
    class_number = (await state.get_data())['class_number']
    Student().set('int', 'class', class_number, message.from_user.id)
    await message.answer('Вы зарегистрированы как ученик', reply_markup=global_menu_student.markup)
    await state.set_state(GlobalMenu.student)


@router_command_start.message(F.text == 'На главное меню')
async def _new_student(message: Message, state: FSMContext):
    await state.clear()
    await message.answer('Привет, отличного дня!', reply_markup=global_menu_teacher.markup)
    await state.set_state(GlobalMenu.teacher)
