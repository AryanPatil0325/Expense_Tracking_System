import sqlite3
import os
from global_expense_dict import BASE_DIR

def initialize_database(db_name="expense_transactions.db"):
    directory = os.path.join(BASE_DIR, "database")
    os.makedirs(directory, exist_ok=True)
    path = os.path.join(directory, db_name)
    connection = sqlite3.connect(path)

    # Enable foreign key enforcement for this connection
    connection.execute("PRAGMA foreign_keys = ON")

    if not os.path.isfile(path):
        print(f"Database file {db_name} created successfully...")
    else:
        print(f"{db_name} database already exists...")

    print(f"Connection established with {db_name}")
    return connection


def create_tables():
    conn = initialize_database()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS expense_categories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                category_name TEXT NOT NULL UNIQUE
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS expense_transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                category_id INTEGER NOT NULL,
                amount INTEGER NOT NULL,
                timestamp TEXT NOT NULL,
                FOREIGN KEY (category_id)
                    REFERENCES expense_categories(id)
            )
        """)

        conn.commit()
        print("Tables created successfully...")

    except sqlite3.Error as error:
        conn.rollback()
        print(f"Database error: {error}")

    finally:
        cursor.close()
        conn.close()


con = initialize_database()
create_tables()
cursor = con.cursor()
cursor.execute("PRAGMA table_info(expense_categories)")
print(cursor.fetchall())
cursor.execute("PRAGMA table_info(expense_transactions)")
print(cursor.fetchall())

cursor.close()
con.close()