from sqlite3 import connect
from config import PATH_TO_DB_TASK

class TaskBank():
    def get_task(self, number):
        with connect(PATH_TO_DB_TASK) as db:
            cursor = db.cursor()
            cursor.execute(f"SELECT * FROM task_bank WHERE number = {number}")
            self.task = cursor.fetchall()
            
