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