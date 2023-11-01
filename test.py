import sqlite3
import contextlib

with contextlib.closing(sqlite3.connect('database/database.db')) as connection:
    with connection as cursor:
        cursor.execute("""

            INSERT INTO todo (title, description, status) VALUES ('Помыть верблюда 1', 'Помыть верблюда 1 Помыть верблюда 1', 'false');

                        """)