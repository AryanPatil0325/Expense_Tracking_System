from global_expense_dict import EXPENSE_CATEGORY
import json

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
                expense_category = input("Enter expense category: ")
                if expense_category not in EXPENSE_CATEGORY:
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


def print_all_expense_types_loaded():
    """Function which will print all the expense categories added to the EXPENSE_CATEGORY"""
    if len(EXPENSE_CATEGORY) == 0:
        return "No Expense Categories present. Add one to continue"
    print("""|-------------------------------------|
                        Expense Categories Available
    |-------------------------------------|
    """)
    for cat in EXPENSE_CATEGORY.keys():
        print(cat)
    print("|-----------------------------------|")


def input_amount_for_expense_cat():
    """Function to take input from user on amount spend on expense type"""
    if len(EXPENSE_CATEGORY)==0:
        print("No Expense Categories present. Add one to continue")

    print_all_expense_types_loaded()
    exit= True
    while exit:
        expense_cat = input("Enter the Expense Category: ")
        expense_amt = float(input("Amount spend: "))
        
        if expense_amt<0:
            return "Amount cannot be negative.Re-enter the amount"

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
    print("""|-------------------------------------|
                       Current Expenses
    |-------------------------------------|
        """)
    total_expense = 0
    for cat,value in EXPENSE_CATEGORY.items():
        print(f"{cat} : Rs.{value}")
        total_expense+=value
    
    print("|-----------------------------------|")
    print(f"Total Amount: {total_expense}")
    print("|-----------------------------------|")
        