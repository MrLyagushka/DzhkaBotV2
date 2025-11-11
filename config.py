import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

PATH_TO_DB_USERS = "db/users.db"

PATH_TO_DB_TASK = "db/test.db"

index_id_teacher, index_id_student, index_id_task, index_answer, index_text = 0, 1, 2, 3, 4
