from global_expense_dict import EXPENSE_CATEGORY, BASE_DIR, CATEGORY_ID_MAP
from database import initialize_database, load_monthly_expense_in_db,CONN
import sqlite3
from datetime import datetime
import math

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
            continue

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
                        # Update the EXPENSE_CATEGORY
                        EXPENSE_CATEGORY[expense_category]=0
                        # Update the CATEGORY_ID_MAP
                        cursor.execute("SELECT * FROM expense_categories")
                        rows = cursor.fetchall()
                        for data in rows:
                            CATEGORY_ID_MAP[data[1]] = data[0]
                        print(f"{expense_category} stored successfully..")
                        
                    except sqlite3.Error as error:
                        CONN.rollback()
                        print(f"Error type: {type(error).__name__}")
                        print(f"Error message: {repr(error)}")

                    finally:
                        cursor.close()
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
        return
    
    print_all_expense_types_loaded()
    running= True
    while running:
        
        expense_cat = input("Enter the Expense Category: ").strip().lower()
        if not expense_cat.isalpha():
            print("Expense Category should contain alphabets only.")    
            continue

        if expense_cat not in EXPENSE_CATEGORY:
            print("No such expense category available, please enter a valid category")
            continue

        while True:
            try:    
                expense_amt = float(input("Amount spend: "))
                if expense_amt<=0:
                    print("Amount cannot be negative or zero.Re-enter the amount") 
                    continue
                
                if math.isinf(expense_amt) or math.isnan(expense_amt):
                    print("Please enter a valid finite amount")
                    continue

                break
                
            except ValueError :
                print("Invalid input. Please enter a valid numeric amount.")
                continue
 
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        try:
            load_monthly_expense_in_db(
                category_id=CATEGORY_ID_MAP[expense_cat],
                amount=expense_amt,
                timestamp=timestamp,
            )
        except sqlite3.Error as error:
            print(f"Could not save the expense ({type(error).__name__}). Nothing was recorded, please try again.")
            break
        # load_monthly_expense_in_db(category_id=category_id,amount=expense_amt,timestamp=timestamp)
        EXPENSE_CATEGORY[expense_cat]+=expense_amt
        print(f"Amount: {expense_amt} added to Expense Category: {expense_cat}")

        to_exit = input("Want to exit?...(Press q/z)")
        running = False if to_exit.lower().strip() in ('q','z') else True


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

    