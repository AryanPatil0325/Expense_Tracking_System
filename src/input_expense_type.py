from global_expense_dict import EXPENSE_CATEGORY, BASE_DIR
import json
import os

def input_expense_type():
    """Function that will take input from user about expense type and store it in an json file inside expense_type directory"""
    
    filename = "expense_categories.json"
    file_exists = True
    while file_exists:
        print("""Choose anyone from below:
            1. Enter expense category
            2. Exit
        """)
        option_selected = int(input("Your choice... "))
        match(option_selected):
            case 1:
                expense_category = input("Enter expense category: ").lower()
                if not expense_category.isalpha():
                    print(f"Invalid Expense Category: {expense_category}. Expense Category should contain only alphabets")
                elif expense_category not in EXPENSE_CATEGORY:
                    EXPENSE_CATEGORY[expense_category] = 0
                    print(f"{expense_category} stored successfully")
                else:
                    print(f"Expense category: {expense_category} exists...")
            case 2:
                path = "Expense_Tracking_System/expense_type"
                with open(f"{path}/{filename}",'w') as file:
                    json.dump(list(EXPENSE_CATEGORY.keys()),file,indent=4)
                file_exists = False
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
        expense_cat = input("Enter the Expense Category: ").lower()
        if not expense_cat.isalpha():
            print("Expense Category should contain alphabets only.")
            return
        expense_amt = float(input("Amount spend: "))
        if expense_amt<0:
            print("Amount cannot be negative.Re-enter the amount") 
            return

        if expense_cat.isalpha() and len(EXPENSE_CATEGORY)!=0 and expense_cat in EXPENSE_CATEGORY:
            EXPENSE_CATEGORY[expense_cat]+=expense_amt
            print(f"Amount: {expense_amt} added to Expense Category: {expense_cat}")
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

def load_existing_expense_categories():
    path = os.path.join(BASE_DIR,"expense_type","expense_categories.json")
    if os.path.isfile(path):
        print("Loading the existing expense categories...")
        with open(path,'r') as file:
            data = json.load(file)
            print("File loaded successfully")
        for expense_cat in data:
            EXPENSE_CATEGORY[expense_cat]=0
        print("Expense category loaded and initialized")
    