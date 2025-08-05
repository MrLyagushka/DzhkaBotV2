from utils.menu import Menu


def generate_keyboard_choose_a_student(tasks, first_index):
    """
    tasks получить из GetTask(id_student).task_student
    :param tasks:
    :param first_index:
    :return:
    """
    choose_a_student = Menu('inline', 2)
    if len(tasks) > 3:
        choose_a_student.new_button(f"{tasks[first_index]}", row_number=1, callback_data=f"{tasks[first_index]}")
        choose_a_student.new_button(f"{tasks[first_index + 1]}", row_number=1, callback_data=f"{tasks[first_index + 1]}")
        choose_a_student.new_button(f"{tasks[first_index + 2]}", row_number=1, callback_data=f"{tasks[first_index + 2]}")

        choose_a_student.new_button('<', row_number=2, callback_data=f'<:{first_index}')
        choose_a_student.new_button('>', row_number=2, callback_data=f'>:{first_index}')
    else:
        for task in tasks:
            choose_a_student.new_button(f"{task}", row_number=1, callback_data=f"{task}")