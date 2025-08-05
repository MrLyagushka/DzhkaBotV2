from sqlite3 import connect
from config import PATH_TO_DB_TASK


class NewTest:
    def __init__(self,id_teacher: int, id_student: int, id_task: int, text: str):
        with connect(PATH_TO_DB_TASK) as db:
            cursor = db.cursor()
            cursor.execute(f'INSERT INTO test (id_teacher, id_student, id_task, answer, text) VALUES ({id_teacher}, {id_student}, {id_task}, "0", "{text}")')
            db.commit()