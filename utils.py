
from datetime import datetime
import re, uuid
import constants
import data_manager


#fectching the current date automatically
def current_date():
    return datetime.now().date().strftime("%Y-%m-%d")

#validate date formate for uniformity
def validate_date(date_str):
    try:
        datetime.strptime(date_str,constants.DATE_FORMAT)
        return True
    except ValueError:
        return False

#sorting expense by date
def sort_by_date(list_to_sort):
    sorted_list = sorted(
                list_to_sort,
                key= lambda x: datetime.strptime(x["date"], "%Y-%m-%d")
            )
    return sorted_list

#validate amount
def validate_amount(amount):
    try:
        amt = float(amount)
        return amt >= 0
    except (ValueError,TypeError):
        return False

#validate category
def validate_category(category):
    return category in constants.VALID_CATEGORY

#generating uniq id for every entry
def generate_unique_id(expenses_list):
    # Using UUID4 ensures practically no collisions
    new_id = str(uuid.uuid4())
    existing_ids = {e["id"] for e in expenses_list}
    while new_id in existing_ids:
        new_id = str(uuid.uuid4())
    return new_id

#validate the inputs
def validate_input(prompt,function,error_message ="Wrong entry,Try again."):
    while True:
        user_input = input(prompt).strip()
        if function(user_input):
            return user_input
        else:
            print(error_message)
