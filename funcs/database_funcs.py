import psycopg2

from config import database


def ConnectToDataBase():
    connection = psycopg2.connect(
        dbname=database[0],
        user=database[1],
        password=database[2],
        port=database[3],
        host=database[4]
    )
    return connection


def create_tables():
    connection = ConnectToDataBase()
    with connection.cursor() as cursor:
        cursor.execute(
            """
        CREATE TABLE IF NOT EXISTS notes (
            id serial PRIMARY KEY,
            title varchar NOT NULL,
            user_id bigint NOT NULL,
            category_id bigint NOT NULL
        );
            """)
        cursor.execute(
            """
        CREATE TABLE IF NOT EXISTS categories (
            id serial PRIMARY KEY,
            title varchar NOT NULL
        );
            """)
        cursor.execute("SELECT * FROM categories")
        categories = cursor.fetchone()
        if not categories:
            for category in ["personal", "work", "study", "day_plans", "other", "all"]:
                cursor.execute("INSERT INTO categories (title) VALUES ((%s))", (category,))
        cursor.execute(
            """
        CREATE TABLE IF NOT EXISTS users (
            id serial PRIMARY KEY,
            telegram_id bigint NOT NULL,
            name varchar NOT NULL
        );
            """
        )
    connection.commit()
    connection.close()


def add_user_to_db(telegram_id, name):
    connection = ConnectToDataBase()
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM users WHERE telegram_id = (%s)", (telegram_id,))
        result = cursor.fetchone()
        if not result:
            cursor.execute("INSERT INTO users (telegram_id, name) VALUES ((%s), (%s))", (telegram_id, name))
    connection.commit()
    connection.close()


def category_id(category):
    connection = ConnectToDataBase()
    with connection.cursor() as cursor:
        cursor.execute("SELECT categories.id FROM categories WHERE categories.title = (%s)", (category, ))
        result = cursor.fetchone()
    connection.commit()
    connection.close()
    return result[0]


def user_id(telegram_id):
    connection = ConnectToDataBase()
    with connection.cursor() as cursor:
        cursor.execute("SELECT users.id FROM users WHERE users.telegram_id = (%s)", (telegram_id,))
        result = cursor.fetchone()
    connection.commit()
    connection.close()
    return result[0]


def add_note_to_db(note: str, telegram_id: int, category: str):
    connection = ConnectToDataBase()
    with connection.cursor() as cursor:
        cursor.execute(
            "INSERT INTO notes (title, user_id, category_id) VALUES ((%s), (%s), (%s))",
            (note, user_id(telegram_id), category_id(category))
        )
    connection.commit()
    connection.close()


def get_notes_from_category(category, telegram_id):
    connection = ConnectToDataBase()
    with connection.cursor() as cursor:
        if category == "all":
            cursor.execute(
                """SELECT notes.title, categories.title FROM notes 
                JOIN categories on categories.id = notes.category_id
                WHERE notes.user_id = (%s)""",
                (user_id(telegram_id), ))
            result = cursor.fetchall()
        else:
            cursor.execute(
                "SELECT notes.title FROM notes WHERE notes.user_id = (%s) and notes.category_id = (%s)",
                (user_id(telegram_id), category_id(category)))
            result = cursor.fetchall()
    connection.commit()
    connection.close()
    return result


def delete_notes_db(category, telegram_id, notes=None):
    connection = ConnectToDataBase()
    id_category = category_id(category)
    id_user = user_id(telegram_id)
    with connection.cursor() as cursor:
        if not notes:
            cursor.execute("DELETE FROM notes WHERE category_id = (%s) and user_id = (%s)", (id_category, id_user))
        else:
            for note in notes:
                cursor.execute("DELETE FROM notes WHERE category_id = (%s) and title = (%s) and user_id = (%s)", (id_category, note, id_user))
    connection.commit()
    connection.close()


def delete_all_notes_from_user_db(telegram_id):
    connection = ConnectToDataBase()
    with connection.cursor() as cursor:
        cursor.execute("DELETE FROM notes WHERE user_id = (%s)", (user_id(telegram_id),))
    connection.commit()
    connection.close()


if __name__ == "__main__":
    category_id("work")
