from sqlite3 import connect
from typing_extensions import Literal

from config import PATH_TO_DB_TASK, PATH_TO_DB_USERS

class Teacher():
    def __init__(self):
        with connect(PATH_TO_DB_USERS) as db:
            cursor = db.cursor()
            cursor.execute(f"SELECT * FROM teacher")
            self.teachers_id = [x[0] for x in cursor.fetchall()]

    def get_statistics(self, id_teacher):
        """
        Возвращает количество ответов на задания и количество правильных ответов
        Так же количество учеников и данные учеников"""
        with connect(PATH_TO_DB_TASK) as db:
            cursor = db.cursor()
            cursor.execute(f"SELECT answer FROM test WHERE id_teacher = {id_teacher}")
            answer = cursor.fetchall()
            self.number_of_task = len(answer)
            self.correct_answer = sum(map(lambda x: x[0], answer))

        with connect(PATH_TO_DB_USERS) as db:
            cursor = db.cursor()
            cursor.execute(f"SELECT * FROM student WHERE id = {id_teacher}")
            answer = cursor.fetchall()
            self.students_id = set(map(lambda x: x[0], cursor.fetchall()))
            self.number_of_students = len(self.students_id)
            cursor.execute(f"SELECT name FROM teacher WHERE id = {id_teacher}")
            self.name = cursor.fetchall()[0][0]

    def new_teacher(self, id: int):
        self.teacher = self.teachers_id
        self.student = list(map(lambda x: x[0], Student().student))
        self.id = id
        if self.id not in self.teacher and self.id not in self.student:
            with connect(PATH_TO_DB_USERS) as db:
                cursor = db.cursor()
                cursor.execute(f"INSERT INTO teacher (id, name, date, description) VALUES ({id}, 'teacher', 01010001, 'description')")
                db.commit()

    def check(self):
        if self.id not in self.teacher and self.id not in self.student:
            return True
        return False
    
    def set(self, format: Literal["str", "int"], column, value, id_teacher):
        with connect(PATH_TO_DB_USERS) as db:
            cursor = db.cursor()
            if format == 'str':
                cursor.execute(f"UPDATE teacher SET {column} = '{value}' WHERE id = {id_teacher}")
            elif format == 'int':
                cursor.execute(f"UPDATE teacher SET {column} = {value} WHERE id = {id_teacher}")
            db.commit()
            
class Student():
    def __init__(self):
        with connect(PATH_TO_DB_USERS) as db:
            cursor = db.cursor()
            cursor.execute("SELECT * FROM student")
            self.student = cursor.fetchall()

    def get_statistics(self, id_student):
        with connect(PATH_TO_DB_TASK) as db:
            cursor = db.cursor()
            cursor.execute(f"SELECT answer FROM test WHERE id_student = {id_student}")
            answer = cursor.fetchall()
            self.number_of_task = len(answer)
            self.correct_answer = sum(map(lambda x: x[0], answer)) 
    
    def new_student(self, id: int):
        self.teacher = Teacher().teachers_id
        self.student = list(map(lambda x: x[0], self.student))
        self.id = id
        if self.id not in self.teacher and id not in self.student:
            with connect(PATH_TO_DB_USERS) as db:
                cursor = db.cursor()
                cursor.execute(f"INSERT INTO student (id, id_teacher, class, name) VALUES ({id}, 0, 11, 'student')")
                db.commit()

    def check(self):
        if self.id not in self.teacher and self.id not in self.student:
            return True
        return False
    
    def update_student(self, id_teacher: int, id_student: int):
        with connect(PATH_TO_DB_USERS) as db:
            cursor = db.cursor()
            cursor.execute(f"UPDATE student SET id_teacher = ? WHERE id = ?", (id_teacher, id_student))
            db.commit()
    
    def set(self, format: Literal["str", "int"], column, value, id_student):
        with connect(PATH_TO_DB_USERS) as db:
            cursor = db.cursor()
            if format == 'str':
                cursor.execute(f"UPDATE student SET {column} = '{value}' WHERE id = {id_student}")
            elif format == 'int':
                cursor.execute(f"UPDATE student SET {column} = {value} WHERE id = {id_student}")
            db.commit()