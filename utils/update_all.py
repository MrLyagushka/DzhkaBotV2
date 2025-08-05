from sqlite3 import connect

from config import PATH_TO_DB_TASK, PATH_TO_DB_USERS

class Update:
    def update_poly_student_new_student(self, id_teacher: int, id_student: int):
        with connect(PATH_TO_DB_USERS) as db:
            cursor = db.cursor()
            cursor.execute(f"UPDATE student SET idTeacher = ? WHERE id = ?", (id_teacher, id_student))
            db.commit()

    def update_poly_teacher_new_student(self, id_teacher: int):
        with connect(PATH_TO_DB_USERS) as db:
            cursor = db.cursor()
            cursor.execute(f"UPDATE teacher SET numbersOfStudent = numbersOfStudent + 1 WHERE id = {id_teacher}")
            db.commit()


    def update_poly_test_answer(self, answer, id_task):
        with connect(PATH_TO_DB_TASK) as db:
            cursor = db.cursor()
            answer = ''.join(sorted(str(answer)))
            cursor.execute(f"UPDATE test SET answer = 1 WHERE id_task = {id_task}")
            db.commit()

