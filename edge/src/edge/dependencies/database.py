from edge.database.db import Database

db = Database()


def get_db() -> Database:
    return db
