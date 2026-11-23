import sqlite3

conn = sqlite3.connect("Expense_Tracking_System/database/expense_transactions.db")
cursor = conn.cursor()
cursor.execute("DELETE FROM expense_categories WHERE id = 5")
conn.commit()
# print("Connection created..")
# # cursor.execute("""
# # CREATE TABLE IF NOT EXISTS students(
# #     ID INTEGER PRIMARY KEY AUTOINCREMENT,
# #     NAME TEXT NOT NULL,
# #     AGE INTEGER,
# #     GRADE TEXT
# # )
# # """)
# # constants
# # cursor.execute("Drop Table students")
# # cursor.execute("Select * from students")
# # print(cursor.fetchone())


# cursor.execute("""
# CREATE TABLE if not exists expense_categories (
#     id INTEGER PRIMARY KEY AUTOINCREMENT,
#     category_name TEXT NOT NULL UNIQUE
# )
# """)

# conn.commit()

# cursor.execute("PRAGMA table_info(expense_categories);") # print the metadata
# print(cursor.fetchall())

# UPDATE expense_categories
# SET category_name = ?
# WHERE id = ?;

# DELETE FROM expense_categories
# WHERE id = ?;

# -------------------------------------Transaction and Rollback-------------------------------------------------------------------
# try:
#     cursor.execute(
#         "INSERT INTO expense_categories (category_name) VALUES (?)",
#         ("Health",)
#     )

#     cursor.execute(
#         "INSERT INTO expense_categories (category_name) VALUES (?)",
#         ("Utilities",)
#     )

#     conn.commit()
#     print("Transaction completed successfully.")

# except sqlite3.IntegrityError as e:
#     conn.rollback()
#     print(f"Transaction failed: {e}")
