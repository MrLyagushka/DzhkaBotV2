from sqlite3 import connect
from config import PATH_TO_DB_TASK

class TaskBank():
    def __init__(self):
        pass
    def get_task(self, number):
        with connect(PATH_TO_DB_TASK) as db:
            cursor = db.cursor()
            cursor.execute(f"SELECT * FROM task_bank WHERE number = {number}")
            self.number = cursor.fetchall()
        return self.number

    def get_task_with_id(self, number, id_task):
        with connect(PATH_TO_DB_TASK) as db:
            cursor = db.cursor()
            cursor.execute(f"SELECT * FROM task_bank WHERE number = {number} AND id_task= {id_task}")
            self.number = cursor.fetchall()
        return self.number
    
            
