from input_expense_type import input_expense_type, print_all_expense_types_loaded,input_amount_for_expense_cat,current_expense
from loading_data import dump_existing_data, view_till_date_history

print("-"*50)
print("-- Welcome to Expense Tracking System --")
print("-"*50)

while True:
    print("""
    |--------------------------------------------|
    | 1. Add Expense Type                        |
    | 2. Add Expense                             |
    | 3. View Current Expenses                   |
    | 4. Exit                                    |
    |--------------------------------------------|
""")
    try:
        choice = int(input("Enter your choice: "))
        match(choice):
            case 1:
                print_all_expense_types_loaded()
                input_expense_type()
            case 2:
                input_amount_for_expense_cat()
            case 3:
                current_expense()
            case 4:
                dump_existing_data()
                view_till_date_history()
                print("Thanks for using Expense Tracker System...")
                break
            case _:
                print("Invalid Choice...Re-enter your choice")
    except Exception as e:
        print(f"Error: {e}")