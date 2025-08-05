from sqlite3 import connect

from config import PATH_TO_DB_TASK

class GetStatisticsStudent():
    def __init__(self, id_student):
        with connect(PATH_TO_DB_TASK) as db:
            cursor = db.cursor()
            cursor.execute(f"SELECT answer FROM test WHERE id_student = {id_student}")
            answer = cursor.fetchall()
        self.number_of_task = len(answer)
        self.correct_answer = sum(map(lambda x: x[0], answer))
