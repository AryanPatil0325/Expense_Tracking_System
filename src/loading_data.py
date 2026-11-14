import os, json
from datetime import date
from expense_file_creation import create_json_files_on_monthly_basis
from global_expense_dict import EXPENSE_CATEGORY,BASE_DIR

def load_expense_file(filename:str):
    path = os.path.join(BASE_DIR,"expense_type", filename)
    if os.path.isfile(path):
        with open(path,'r') as file:
            data = json.load(file)
            return data
    else:
        raise FileNotFoundError(f"{filename} file not found")
    # return data

def dump_existing_data():
    filename = create_json_files_on_monthly_basis()
    path = os.path.join(BASE_DIR,"expense_type",filename)
    # Case 1: File is empty -> add the records
    data = load_expense_file(filename)
    
    if len(data) == 0:
        data.append({"date":str(date.today().isoformat()),"expenses":EXPENSE_CATEGORY.copy()})
    else:
    # Case 2: File exists with current record
        current_record_present = False
        for record in data:
            if record['date'] == str(date.today().isoformat()):
                current_record_present = True
                for new_expense_type in EXPENSE_CATEGORY.keys():
                    if new_expense_type not in record['expenses']:
                        record['expenses'][new_expense_type] = 0
                    record['expenses'][new_expense_type] += EXPENSE_CATEGORY[new_expense_type]
                print("Record updated successfully")
                break

        # Case 3: File exists with no record
        if not current_record_present:
            data.append({"date":str(date.today().isoformat()),"expenses":EXPENSE_CATEGORY})

    # Load the new data to file
    with open(path,'w') as file:
        json.dump(data,file,indent=4)
        print(f"Data updated successfully in {filename}")

def view_till_date_history():
    filename= create_json_files_on_monthly_basis()
    data = load_expense_file(filename)
    total_history = {}
    for record in data:
        for cat,val in record['expenses'].items():
            total_history[cat] = (total_history.get(cat,0))+val
    print("|----------------------------------------|")
    print("               Total Expense              ")
    print("|----------------------------------------|")
    for category,amt in total_history.items():
        print(f"{category}: {amt}")
    print("|----------------------------------------|")
    print(f"Total Amount: Rs.{sum(total_history.values())}")


                