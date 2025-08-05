from utils.menu import Menu

global_menu_teacher = Menu('reply', 2)
global_menu_teacher.new_button('Добавить ученика', 1)
global_menu_teacher.new_button('Добавить тест', 1)
global_menu_teacher.new_button('Банк заданий', 1)
global_menu_teacher.new_button('Профиль', 2)

global_menu_student = Menu('reply', 2)
global_menu_student.new_button('Решать тесты', 1)
global_menu_student.new_button('Профиль', 2)

global_menu_first_visit = Menu('reply', 2)
global_menu_first_visit.new_button('Я учитель', 1)
global_menu_first_visit.new_button('Я ученик', 2)