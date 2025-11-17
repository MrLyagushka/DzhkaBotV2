from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
import logging
from aiogram.fsm.context import FSMContext

from utils.template import DinamicKeyboard, MyCallbackData
from filters.is_student import IsStudent
from filters.is_teacher import IsTeacher
from handlers.global_menu import GlobalMenu
from keyboards.global_menu import global_menu_student, global_menu_teacher

router_service_handlers = Router()


@router_service_handlers.callback_query(MyCallbackData.filter())
async def on_the_what(callback: CallbackQuery, callback_data: MyCallbackData):
    await callback.answer()
    first_index = callback_data.first_index
    if callback_data.callback_data == '<':
        first_index = first_index - 1 if first_index > 0 else first_index
    elif callback_data.callback_data == '>':
        first_index = first_index + 1 if callback_data.len_button_list > first_index + callback_data.row*callback_data.column else first_index
    if first_index != callback_data.first_index:
        await callback.message.edit_reply_markup(inline_message_id=callback.inline_message_id,
                                             reply_markup=DinamicKeyboard(row=callback_data.row,
                                                                          column=callback_data.column,
                                                                          is_always_bigger_column_multiply_row=callback_data.is_always_bigger,
                                                                          first_index=first_index,
                                                                          button_info=callback_data.button_info).generate_keyboard())


@router_service_handlers.message(F.text and IsTeacher())
async def authorizetion(message: Message, state: FSMContext):
    await state.set_state(GlobalMenu.teacher)
    await message.answer('Вы авторизованы как учитель', reply_markup=global_menu_teacher.markup)

@router_service_handlers.message(F.text and IsStudent())
async def authorizetion(message: Message, state: FSMContext):
    await state.set_state(GlobalMenu.student)
    await message.answer('Вы авторизованы как ученик', reply_markup=global_menu_student.markup)

