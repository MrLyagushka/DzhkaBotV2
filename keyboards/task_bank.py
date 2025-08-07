from utils.menu import Menu

choose_next_step = Menu('reply', 1)

choose_next_step.new_button('Посмотреть задания', row_number=1)
choose_next_step.new_button('Добавить задание', row_number=1)
choose_next_step.markup