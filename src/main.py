from input_expense_type import input_expense_type, print_all_expense_types_loaded,input_amount_for_expense_cat,current_expense, load_existing_expense_categories
from loading_data import dump_existing_data, view_till_date_history

def display_menu():
    print("-"*50)
    print("-- Welcome to Expense Tracking System --")
    print("-"*50)
    print("""
        |--------------------------------------------|
        | 1. Add Expense Type                        |
        | 2. Add Expense                             |
        | 3. View Current Expenses                   |
        | 4. Exit                                    |
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
                dump_existing_data()
                view_till_date_history()
                print("Thanks for using Expense Tracker System...")
            case _:
                print("Invalid Choice...Re-enter your choice")
    
                
    
def main():
    # initialize the existing expense category
    load_existing_expense_categories()
    # display menu and handle choices
    while True:
        try:
            display_menu()
            choice = int(input("Enter you choice: "))
            handle_menu_choice(choice)
            if choice == 4:
                break
        except ValueError as e:
                print(f"Select choice as per the displayed menu: {e}")
        

if __name__ == "__main__":
    main()