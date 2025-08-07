from sqlite3 import connect
from config import PATH_TO_DB_TASK


class Task:
    def new_task(self, id_teacher: int, id_student: int, id_task: int, text: str):
        with connect(PATH_TO_DB_TASK) as db:
            cursor = db.cursor()
            cursor.execute(f'INSERT INTO test (id_teacher, id_student, id_task, answer, text) VALUES ({id_teacher}, {id_student}, {id_task}, "0", "{text}")')
            db.commit()
    
    def get_task(self, id_student = 0, id_task = 0):
        with connect(PATH_TO_DB_TASK) as db:
            cursor = db.cursor()
            cursor.execute("SELECT id_task FROM test ORDER BY id_task DESC LIMIT 1")
            self.number_last_line = cursor.fetchall()[0][0]
            if id_student != 0:
                cursor.execute(f"SELECT * FROM test WHERE id_student = {id_student}")
                self.task_student = cursor.fetchall()
            if id_task != 0:
                cursor.execute(f"SELECT * FROM test WHERE id_task = {id_task}")
                self.task_number_n = cursor.fetchall()
                self.task_number_n_answer = self.task_number_n[0][index_text].split('_')[-1].split('ОТВЕТ')[1].split()[0]
    
    def update_task(self, answer, id_task):
        with connect(PATH_TO_DB_TASK) as db:
            cursor = db.cursor()
            answer = ''.join(sorted(str(answer)))
            cursor.execute(f"UPDATE test SET answer = 1 WHERE id_task = {id_task}")
            db.commit()