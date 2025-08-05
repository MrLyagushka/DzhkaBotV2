from sqlite3 import connect

from config import PATH_TO_DB_USERS


class GetStudent:
    def __init__(self):
        with connect(PATH_TO_DB_USERS) as db:
            cursor = db.cursor()
            cursor.execute("SELECT * FROM student")
            self.student = cursor.fetchall()
