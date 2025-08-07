from aiogram import Router, F
from aiogram.types import CallbackQuery
from utils.template import DinamicKeyboard, MyCallbackData

router_service_handlers = Router()


@router_service_handlers.callback_query(MyCallbackData.filter())
async def on_the_what(callback: CallbackQuery, callback_data: MyCallbackData):
    task = []
    first_index = callback_data.first_index
    if callback_data.callback_data == '<':
        first_index -= 1 if first_index > 0 else 0
    if callback_data.callback_data == '>':
        first_index += 1 if len(task) > first_index else len(task)
    await callback.answer()
    await callback.message.edit_reply_markup(inline_message_id=callback.inline_message_id,
                                             reply_markup=DinamicKeyboard(row=callback_data.row,
                                                                          column=callback_data.column,
                                                                          is_always_bigger_column_multiply_row=callback_data.is_always_bigger,
                                                                          first_index=callback_data.first_index,
                                                                          button_list=task).generate_keyboard())

