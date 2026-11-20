from input_expense_type import input_expense_type, print_all_expense_types_loaded,input_amount_for_expense_cat,current_expense
from loading_data import dump_existing_data, view_till_date_history
from database import sqlite_cat_load_to_expense_categories, create_tables,CONN

def display_menu():
    print("-"*50)
    print("-- Welcome to Expense Tracking System --")
    print("-"*50)
    print("""
        |--------------------------------------------|
        | 1. Add Expense Type                        |
        | 2. Add Expense                             |
        | 3. View Current Expenses                   |
        | 4. View Current Month Expenses             |
        | 5. Exit                                    |
        |--------------------------------------------|
    """)

def handle_menu_choice(choice:int):
        match(choice):
            case 1:
                print_all_expense_types_loaded()
                input_expense_type()
            case 2:
                input_amount_for_expense_cat()
            case 3:
                current_expense()
            case 4:
                view_till_date_history()
            case 5:
                # dump_existing_data()
                print("Thanks for using Expense Tracker System...")
            case _:
                print("Invalid Choice...Re-enter your choice")

                    
    
def main():

    # display menu and handle choices
    try:
        # Table created
        create_tables()
        # initialize the existing expense category
        sqlite_cat_load_to_expense_categories()
        while True:
            try:
                display_menu()
                choice = int(input("Enter you choice: "))
                handle_menu_choice(choice)
                if choice == 5:
                    break
            except ValueError:
                print("Please enter a valid choice..")
            except KeyboardInterrupt:
                print("Application Interrupted by user")
                break
    finally:
        # store the existing data 
        dump_existing_data()
        CONN.close()

if __name__ == "__main__":
    main()