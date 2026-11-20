from global_expense_dict import EXPENSE_CATEGORY, BASE_DIR, CATEGORY_ID_MAP
from database import initialize_database, load_monthly_expense_in_db,CONN
import sqlite3
from datetime import datetime

def input_expense_type():
    """Function that will take input from user about expense type and store it in an json file inside expense_type directory"""
    
    filename = "expense_categories.json"
    file_exists = True
    while file_exists:
        print("""Choose anyone from below:
            1. Enter expense category
            2. Exit
        """)
        try:
            option_selected = int(input("Your choice... "))
        except ValueError:
            print("Please enter a valid numeric input from the displayed options.")

        match(option_selected):
            case 1:
                expense_category = input("Enter expense category: ").strip().lower()
                if not expense_category.isalpha():
                    print(f"Invalid Expense Category: {expense_category}. Expense Category should contain only alphabets")
                elif expense_category in EXPENSE_CATEGORY:
                    print(f"Expense category: {expense_category} exists...")
                else:
                    
                    cursor = CONN.cursor()
                    try:
                        cursor.execute("""
                            INSERT OR IGNORE INTO expense_categories(category_name) Values(?)
                    """,(expense_category,))

                        CONN.commit()
                        EXPENSE_CATEGORY[expense_category]=0
                        print(f"{expense_category} stored successfully..")
                    except sqlite3.Error as error:
                        CONN.rollback()
                        print(f"Error type: {type(error).__name__}")
                        print(f"Error message: {repr(error)}")
            case 2:
                print("Exiting Category Management..")
                break
            case _:
                print("Invalid choice...select appropriate option")


def print_all_expense_types_loaded():
    """Function which will print all the expense categories added to the EXPENSE_CATEGORY"""
    if len(EXPENSE_CATEGORY) == 0:
        return "No Expense Categories present. Add one to continue"
    print("|-------------------------------------|")
    print("     Expense Categories Available      ")                   
    print("|-------------------------------------|")
    for cat in EXPENSE_CATEGORY.keys():
        print(cat.title())
    print("|-----------------------------------|")


def input_amount_for_expense_cat():
    """Function to take input from user on amount spend on expense type"""
    if len(EXPENSE_CATEGORY)==0:
        print("No Expense Categories present. Add one to continue")

    print_all_expense_types_loaded()
    exit= True
    while exit:
        expense_cat = input("Enter the Expense Category: ").strip().lower()

        if not expense_cat.isalpha():
            print("Expense Category should contain alphabets only.")
            return
        expense_amt = float(input("Amount spend: "))
        if expense_amt<0:
            print("Amount cannot be negative.Re-enter the amount") 
            return

        if expense_cat.isalpha() and len(EXPENSE_CATEGORY)!=0 and expense_cat in EXPENSE_CATEGORY:
            category_id = CATEGORY_ID_MAP[expense_cat.lower()] 
            amount = expense_amt
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            EXPENSE_CATEGORY[expense_cat]+=expense_amt
            print(f"Amount: {expense_amt} added to Expense Category: {expense_cat}")
            load_monthly_expense_in_db(category_id=category_id,amount=amount,timestamp=timestamp)

        else:
            print("Enter valid expense category or no expense category present. Add an Expense Category to continue")
            exit = False
        to_exit = input("Want to exit?...(Press q/z)")
        exit = False if to_exit.lower() in "qz" else True


def current_expense():
    """Function to print the current amount spend by user"""
    print("|-------------------------------------|")
    print("          Current Expenses             ")                  
    print("|-------------------------------------|")
    total_expense = 0
    for cat,value in EXPENSE_CATEGORY.items():
        print(f"{cat.title()} : Rs.{value}")
        total_expense+=value
    
    print("|-----------------------------------|")
    print(f"Total Amount: {total_expense}")
    print("|-----------------------------------|")

    