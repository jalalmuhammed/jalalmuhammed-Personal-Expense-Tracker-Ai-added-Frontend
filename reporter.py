import data_manager
import utils
from collections import defaultdict
from data_manager import load_data

#loading the file
expenses = data_manager.load_data()

#Total expense
def total_expense(expensed):
    total_expenses = 0
    for expense in expensed:
        total_expenses += expense["amount"]
    return total_expenses

#filter by category
def filter_by_category(category):
    category = category.strip()
    try:
        filtered_list = []
        for exp in expenses:
            if exp.get("category") == category:
                filtered_list.append(exp)

        if filtered_list is not None:

            #if expense found in given category,displaying to the user by sorting by the date.
            sorted_list = utils.sort_by_date(filtered_list)

            print(f"Expense Entry Found In The Category '{category}'")
            for exp in sorted_list:
                print(exp)
            print(f"The Grand Total is: {total_expense(sorted_list)}")

        else:
            print(f"No Expense Entry Found In The Category '{category}'")

    except Exception as e:
        print(f"Error Occurred: {e}")


#filter by date range
def filter_by_date(start_date,end_date):
    filtered_exp_list = []

    # checking whether an expense lies between start and end date.
    for expense in expenses:
        if start_date <= expense["date"] <= end_date:
            filtered_exp_list.append(expense)

    #if expense found in the given date range,display them by sorting by date.
    if filtered_exp_list is not None:
        sorted_list = utils.sort_by_date(filtered_exp_list)

        print(f"Expense Found From {start_date} to {end_date}.")
        for exp in sorted_list:
            print(exp)
        print(f"The Grand Total is: {total_expense(sorted_list)}")

    else:
        print(f"No Expense Found From {start_date} to {end_date}.")

#summarize by month
def summarize_by_month():
    summary = defaultdict(float)

    for expense in expenses:
        month_key = expense["date"][:7]
        summary[month_key] += expense["amount"]
    return dict(summary)


#summarize expense by category
def summarize_by_category():
    expenses = load_data()
    summary = {}

    for exp in expenses:
        cat = exp.get("category", "").lower()
        amt = float(exp.get("amount", 0))

        if cat in summary:
            summary[cat] += amt
        else:
            summary[cat] = amt

    return summary
