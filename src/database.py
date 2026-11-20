import sqlite3
import os
import json
from global_expense_dict import BASE_DIR, EXPENSE_CATEGORY, CATEGORY_ID_MAP
from expense_file_creation import create_json_files_on_monthly_basis


def initialize_database(db_name="expense_transactions.db"):
    directory = os.path.join(BASE_DIR, "database")
    os.makedirs(directory, exist_ok=True)
    path = os.path.join(directory, db_name)
    
    connection = sqlite3.connect(path)

    # Enable foreign key enforcement for this connection
    connection.execute("PRAGMA foreign_keys = ON")

    if not path:
        print(f"Database file {db_name} created successfully...")
    else:
        print(f"{db_name} database already exists...")

    print(f"Connection established with {db_name}")
    return connection

# Database Connection
CONN = initialize_database()


def create_tables():
    cursor = CONN.cursor()

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

        CONN.commit()
        print("Tables created successfully...")

    except sqlite3.Error as error:
        CONN.rollback()
        print(f"Error type: {type(error).__name__}")
        print(f"Error message: {repr(error)}")

    finally:
        cursor.close()

def migrate_categories_from_json():
    json_path = os.path.join(BASE_DIR,"expense_type","expense_categories.json")
    if not os.path.exists(json_path):
        raise FileNotFoundError(f"{json_path} file not found")

    # File exists
    with open(json_path,'r') as file:
        # loading the current json file
        data = json.load(file)

    cursor = CONN.cursor()

    try:
        for category in data:
            cursor.execute("""
            INSERT OR IGNORE INTO expense_categories(category_name) VALUES(?)
            """,(category,)
            )
        CONN.commit()
        print("Categories migrated successfully...")
    except sqlite3.Error as error:
        CONN.rollback()
        print(f"Error type: {type(error).__name__}")
        print(f"Error message: {repr(error)}")
    finally:
        cursor.close()

def sqlite_cat_load_to_expense_categories():

    cursor = CONN.cursor()
    try:
        cursor.execute("Select * from expense_categories")
        rows = cursor.fetchall()
        for data in rows:
            EXPENSE_CATEGORY[data[1]] = 0
            CATEGORY_ID_MAP[data[1]] = data[0]
        print("Expense Categories loaded")
    except sqlite3.Error as error:
        CONN.rollback()
        print(f"Error type: {type(error).__name__}")
        print(f"Error message: {repr(error)}")
    finally:
        cursor.close()
        
    
def load_monthly_expense_in_db(category_id,amount,timestamp):
    """
    Function to store the expense data into sqlite3
    Table name: expense_transactions
    columns: id, category_id, amount, timestamp
    """
    cursor = CONN.cursor()

    try:
        cursor.execute("INSERT OR IGNORE INTO expense_transactions(category_id,amount,timestamp) VALUES(?,?,?)",(category_id,amount,timestamp))
        CONN.commit()
        print("Record saved successfully...")
    except sqlite3.Error as error:
        CONN.rollback()
        print(f"Error type: {type(error).__name__}")
        print(f"Error message: {repr(error)}")
    finally:
        cursor.close()

