from utils.menu import Menu

# Переделать с учетом inline кнопок 3x3 и ниже переключение между номерами заданий
# Еще бы сделать класс таких клав

keyboard_list_a_number_of_task = Menu('reply', 6, one_time_keyboard=True)
keyboard_list_a_number_of_task.new_button('№1', 1)
keyboard_list_a_number_of_task.new_button('№2', 1)
keyboard_list_a_number_of_task.new_button('№3', 1)
keyboard_list_a_number_of_task.new_button('№4', 1)
keyboard_list_a_number_of_task.new_button('№5', 1)
keyboard_list_a_number_of_task.new_button('№6', 1)
keyboard_list_a_number_of_task.new_button('№7', 1)

keyboard_list_a_number_of_task.new_button('№8', 2)
keyboard_list_a_number_of_task.new_button('№9', 2)
keyboard_list_a_number_of_task.new_button('№10', 2)
keyboard_list_a_number_of_task.new_button('№11', 2)
keyboard_list_a_number_of_task.new_button('№12', 2)
keyboard_list_a_number_of_task.new_button('№13', 2)
keyboard_list_a_number_of_task.new_button('№14', 2)

keyboard_list_a_number_of_task.new_button('№15', 3)
keyboard_list_a_number_of_task.new_button('№16', 3)
keyboard_list_a_number_of_task.new_button('№17', 3)
keyboard_list_a_number_of_task.new_button('№18', 3)
keyboard_list_a_number_of_task.new_button('№19', 3)
keyboard_list_a_number_of_task.new_button('№20', 3)

keyboard_list_a_number_of_task.new_button('№21', 4)
keyboard_list_a_number_of_task.new_button('№22', 4)
keyboard_list_a_number_of_task.new_button('№23', 4)
keyboard_list_a_number_of_task.new_button('№24', 4)
keyboard_list_a_number_of_task.new_button('№25', 4)
keyboard_list_a_number_of_task.new_button('№26', 4)

keyboard_list_a_number_of_task.new_button('На главное меню', 5)
