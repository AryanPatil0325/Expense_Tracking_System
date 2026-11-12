from input_expense_type import input_expense_type

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
                input_expense_type()
            case 4:
                print("Thanks for using Expense Tracker System...")
                break
            case _:
                print("Invalid Choice...Re-enter your choice")
    except Exception as e:
        print(f"Error: {e}")