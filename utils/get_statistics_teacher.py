from sqlite3 import connect

from config import PATH_TO_DB_TASK, PATH_TO_DB_USERS

class GetStatisticsTeacher():
    def __init__(self, id_teacher):
        with connect(PATH_TO_DB_TASK) as db:
            cursor = db.cursor()
            cursor.execute(f"SELECT answer FROM test WHERE id_teacher = {id_teacher}")
            answer = cursor.fetchall()
        self.number_of_task = len(answer)
        self.correct_answer = sum(map(lambda x: x[0], answer))

        with connect(PATH_TO_DB_USERS) as db:
            cursor = db.cursor()
            cursor.execute(f"SELECT numbersOfStudent FROM teacher WHERE id = {id_teacher}")
            answer = cursor.fetchall()
            self.number_of_students = int(answer[0][0])
            cursor.execute(f"SELECT * FROM student WHERE id = {id_teacher}")
            answer = cursor.fetchall()
            self.students = set(map(lambda x: x[0], cursor.fetchall()))