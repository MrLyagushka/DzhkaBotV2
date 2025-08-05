from sqlite3 import connect

from config import PATH_TO_DB_USERS
from utils.get_teacher import GetTeacher
from utils.get_student import GetStudent

class NewTeacher:
    def __init__(self, id: int):
        self.teacher = GetTeacher().teachers_id
        self.student = list(map(lambda x: x[0],GetStudent().student))
        self.id = id
        if self.id not in self.teacher and self.id not in self.student:
            with connect(PATH_TO_DB_USERS) as db:
                cursor = db.cursor()
                cursor.execute(f"INSERT INTO teacher (id, numbersOfStudent) VALUES ({id}, {0})")
                db.commit()
    def check(self):
        if self.id not in self.teacher and self.id not in self.student:
            return True
        return False