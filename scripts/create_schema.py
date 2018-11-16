import os
import re
import sys

import psycopg2

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.extend([BASE_DIR])

from db.helpers import get_autocommit_connection, call_close
from core.environment import DB_DATA


def handle_db_creation_error(exception):
    message = str(exception)
    database_exists = re.search(r'already exists', message, re.IGNORECASE)
    if database_exists:
        print(message.capitalize())
    else:
        raise exception


def create_database_if_not_exists():
    connection = get_autocommit_connection(
        dbname=DB_DATA['dbname'],
        user=DB_DATA['user'],
        host=DB_DATA['host'],
        password=DB_DATA['password'],
    )
    cursor = connection.cursor()
    try:
        cursor.execute('CREATE DATABASE {};'.format(DB_DATA['dbname']))
    except psycopg2.ProgrammingError as exc:
        handle_db_creation_error(exc)
    finally:
        call_close(cursor, connection)


def create_recipe_table_if_not_exists():
    connection = get_autocommit_connection(**DB_DATA)
    cursor = connection.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS "recipe" (
        id SERIAL PRIMARY KEY,
        name VARCHAR(40) NOT NULL,
        preparation_time INTEGER NOT NULL,
        difficulty INTEGER NOT NULL,
        vegetarian BOOLEAN NOT NULL
    );
    """)

    call_close(cursor, connection)


def create_user_table_if_not_exists():
    connection = get_autocommit_connection(**DB_DATA)
    cursor = connection.cursor()

    cursor.execute('CREATE TABLE IF NOT EXISTS "user" (id SERIAL PRIMARY KEY);')

    call_close(cursor, connection)


def create_rating_table_if_not_exists():
    connection = get_autocommit_connection(**DB_DATA)
    cursor = connection.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS "rating" (
        id SERIAL PRIMARY KEY,
        value INTEGER NOT NULL,
        recipe_id INTEGER NOT NULL,
        FOREIGN KEY (recipe_id) REFERENCES "recipe" (id)
    );
    """)

    call_close(cursor, connection)


if __name__ == '__main__':
    create_database_if_not_exists()
    create_recipe_table_if_not_exists()
    create_user_table_if_not_exists()
    create_rating_table_if_not_exists()
