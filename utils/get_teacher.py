from sqlite3 import connect

from config import PATH_TO_DB_USERS

class GetTeacher:
    def __init__(self, id_teacher = 0):
        with connect(PATH_TO_DB_USERS) as db:
            cursor = db.cursor()

            if id_teacher != 0:
                cursor.execute(f"SELECT * FROM teacher WHERE id = {id_teacher}")
                result = cursor.fetchall()
                self.number_of_students = result[0][1]
                cursor.execute(f"SELECT * FROM student WHERE idTeacher = {id_teacher}")
                result = cursor.fetchall()
                self.id_student = [x[0] for x in result]

            cursor.execute(f"SELECT * FROM teacher")
            self.teachers_id = [x[0] for x in cursor.fetchall()]
