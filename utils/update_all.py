from sqlite3 import connect

from config import PATH_TO_DB_TASK, PATH_TO_DB_USERS

class Update:
    def update_poly_test_answer(self, answer, id_task):
        with connect(PATH_TO_DB_TASK) as db:
            cursor = db.cursor()
            answer = ''.join(sorted(str(answer)))
            cursor.execute(f"UPDATE test SET answer = 1 WHERE id_task = {id_task}")
            db.commit()

