from datetime import date
import os
import json
from global_expense_dict import EXPENSE_DIR

MONTHS = {1:"Jan",2:"Feb",3:"Mar",4:"Apr",5:"May",6:"Jun",7:"Jul",8:"Aug",9:"Sep",10:"Oct",11:"Nov",12:"Dec"}


def create_json_files_on_monthly_basis():
    """Create expense record file on monthly basis."""

    current_year = str(date.today().year)
    current_month_name = MONTHS[date.today().month]

    filename = f"{current_year}_{current_month_name}_expense.json"

    directory = os.path.join(EXPENSE_DIR, "expense_type")
    os.makedirs(directory, exist_ok=True)

    path = os.path.join(directory, filename)

    if not os.path.isfile(path):
        with open(path, 'w') as file:
            json.dump([], file, indent=4)
        print(f"{filename} created successfully.")

    return filename
