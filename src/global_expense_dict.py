import os
EXPENSE_CATEGORY = {}
# __file__ = gives the relative path of the code ** EG: Expense_Tracking_System\src\global_expense_dict.py **
# os.path.abspath(__file__) = gives the abslute path of the code ** EG: C:\Projects\Expense_Tracking_System\src\global_expense_dict.py **
# os.path.dirname = goes one level up -> C:\Projects\Expense_Tracking_System\src
# os.path.dirname = goes one level up -> C:\Projects\Expense_Tracking_System\ -> BASE_DIR
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
