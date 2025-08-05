from sqlite3 import connect

from config import PATH_TO_DB_USERS
from utils.get_student import GetStudent
from utils.get_teacher import GetTeacher

class NewStudent:
    def __init__(self, id: int):
        self.teacher = GetTeacher().teachers_id
        self.student = list(map(lambda x: x[0], GetStudent().student))
        self.id = id
        if self.id not in self.teacher and id not in self.student:
            with connect(PATH_TO_DB_USERS) as db:
                cursor = db.cursor()
                cursor.execute(f"INSERT INTO student (id, idTeacher) VALUES ({id}, {0})")
                db.commit()
    def check(self):
        if self.id not in self.teacher and self.id not in self.student:
            return True
        return False