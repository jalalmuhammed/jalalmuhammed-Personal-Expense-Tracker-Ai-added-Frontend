import json ,os
from json import JSONDecodeError
import utils
from constants import Data_folder, Data_file

def load_data():
    #if folder doesn't exist,creating one
    if not os.path.isdir(Data_folder):
        os.makedirs(Data_folder)

    # if file doesn't exist,creating one
    if not os.path.isfile(Data_file):
        with open(Data_file,"w") as file:
            json.dump([],file)

    #loading existing data
    try:
        with open(Data_file,"r") as file:
            return json.load(file)

    #Handling the decoding error
    except JSONDecodeError:
        with open(Data_file,"w") as file:
            json.dump([], file)
            return []

#save the Data to the file
def save_exp(expense):
    with open(Data_file,"w") as file:
        json.dump(expense,file, indent=4)


#adding new expense record
def add_new_exp(amount,category,description):
    expenses = load_data()
    new_record ={
        "id" : utils.generate_unique_id(expenses),
        "date": utils.current_date(),
        "amount": amount,
        "category": category,
        "description": description
    }
    expenses.append(new_record)
    save_exp(expenses)
    print("Entry Added Successfully.")

#delete an expense

def delete_expense(target_id):
    expenses = load_data()
    target_id = target_id.strip()
    found = False
    new_expense = []

    for expense in expenses:
        current_id = expense.get("id","").strip()
        if current_id == target_id:
            found = True
            continue
        else:
            new_expense.append(expense)

    if found:
        re_assurance = input(f"Are you sure to Delete {target_id} (Y/N): ").lower()
        if re_assurance == "y":
            save_exp(new_expense)
            return True
        else:
            print("Thank You!")
    else:
        print(f"ID: {target_id} Is Not Found.")
        return False

#Edit an expense
def edit_expense(target_id,new_date=None,new_amount=None,new_category=None,new_description= None):
    expense = load_data()
    target_id = target_id.strip()
    found = False
    flag = False

    for exp in expense:
        if exp.get("id") == target_id:
            found = True
            if new_date != '':
                exp["date"] = new_date
                flag = True
            if new_amount != '':
                exp["amount"] = float(new_amount)
                flag = True
            if new_category != '':
                exp["category"] = new_category
                flag = True
            if new_description != '':
                exp["description"] = new_description
                flag = True
            break

    if not found:
        print(f"ID {target_id} is not found")

    if flag:
        save_exp(expense)
        return True
    else:
        return False
