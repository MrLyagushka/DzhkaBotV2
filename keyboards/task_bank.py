from utils.menu import Menu

def choose_next_step(callback_data):
    choose_next_step = Menu('inline', 1)

    choose_next_step.new_button('Посмотреть задания', row_number=1, callback_data=f'see:{callback_data}')
    choose_next_step.new_button('Добавить задание', row_number=1, callback_data=f'new_task:{callback_data}')
    return choose_next_step.markup