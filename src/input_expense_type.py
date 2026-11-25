from global_expense_dict import EXPENSE_CATEGORY, CATEGORY_ID_MAP
from database import load_monthly_expense_in_db,CONN
import sqlite3
from datetime import datetime
import math
import re

def check_valid_expense_category(exp_category:str):
    """Function to check valid expense category entered
    Accepted Conditions:
        Starts with letters 
        Can contain symbols like / - _ & and space
    """
    is_valid_exp_category = True
    if not re.fullmatch(r"[A-Za-z]+(?:[ &_/-][A-Za-z]+)*", exp_category):
        is_valid_exp_category = False
    return is_valid_exp_category

def input_expense_type():
    """Function that will take input from user about expense type and store it in expense_transaction.db"""
    while True:
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
                expense_category = " ".join(input("Enter expense category: ").strip().split()).lower()
                valid_expense_category = check_valid_expense_category(expense_category)
                if not valid_expense_category:
                    print(f"Invalid Expense Category: {expense_category}. Expense Category should contain only alphabets and cant be empty")
                elif expense_category in EXPENSE_CATEGORY:
                    print(f"Expense category: {expense_category} exists...")
                else:
                    cursor = CONN.cursor()
                    try:
                        cursor.execute("""
                            INSERT INTO expense_categories(category_name) Values(?)
                    """,(expense_category,))
                        last_added_id = cursor.lastrowid
                        CONN.commit()

                    except sqlite3.Error as error:
                        CONN.rollback()
                        print(f"Error type: {type(error).__name__}")
                        print(f"Error message: {repr(error)}")

                    else:
                        # Update the data
                        EXPENSE_CATEGORY[expense_category] = 0
                        CATEGORY_ID_MAP[expense_category] = last_added_id
                        print(f"{expense_category.upper()} stored successfully")

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
        print("No Expense Categories present. Add one to continue")
        return
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
        
        expense_cat = " ".join(input("Enter the Expense Category: ").strip().split()).lower()
        valid_expense_category = check_valid_expense_category(expense_cat)
        if not valid_expense_category:
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

    