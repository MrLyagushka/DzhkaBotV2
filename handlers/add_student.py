import logging

from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, ReplyKeyboardRemove

from utils.update_all import Update
from utils.get_student import GetStudent
from keyboards.global_menu import global_menu_teacher

class AddStudent(StatesGroup):
    first = State()
    second = State()
    third = State()
    id_student = State()

router_add_student = Router()

@router_add_student.message(F.text == "Добавить ученика")
async def _add_student1(message: Message, state: FSMContext):
    await state.clear()
    await message.answer('Введите id ученика', reply_markup=ReplyKeyboardRemove())
    await state.set_state(AddStudent.id_student)


@router_add_student.message(AddStudent.id_student)
async def _add_student2(message: Message, state: FSMContext):
    isTrue = True
    await state.update_data(id=message.text)
    if (await state.get_data())['id'] not in ['Добавить тест', 'Профиль']:
        try:
            id_student = int((await state.get_data())['id'])
        except Exception as e:
            await message.answer('Ошибка, попробуйте еще раз', reply_markup=global_menu_teacher.markup)
            logging.info(f'Ошибка в функции _add_student: {e}')
            await state.clear()
            isTrue = False
    else:
        await state.clear()
        isTrue = False
    if isTrue:
        id_teacher = message.from_user.id
        is_add = False
        for student in GetStudent().student:
            if student[0] == id_student and student[1] == 0:
                Update().update_poly_student_new_student(id_student=id_student, id_teacher=id_teacher)
                Update().update_poly_teacher_new_student(id_teacher)
                await message.answer('Ученик успешно добавлен', reply_markup=global_menu_teacher.markup)
                is_add = True
        if not is_add:
            await message.answer('Возникла ошибка, проверьте, зарегистрирован id или привязан', reply_markup=global_menu_teacher.markup)
        await state.clear()
