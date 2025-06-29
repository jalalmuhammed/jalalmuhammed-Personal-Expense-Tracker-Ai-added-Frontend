import data_manager
import utils
import constants
import reporter
import csv
import os

#load expenses list from file
expenses = data_manager.load_data()

def print_menu():
    print(
        """
    Personal Expense Tracker
    ---------------------------
    1. Add new expense
    2. View all expenses
    3. Filter expenses by date range
    4. Filter expenses by category
    5. Edit an expense
    6. Delete an expense
    7. Show monthly summary
    8. Show category summary
    9. Export summaries to CSV
    0. Exit
        """
    )

#Add new expense
def add_entry():
    amount = float(utils.validate_input(
        "Enter Amount: ", utils.validate_amount).strip())
    category = str(utils.validate_input(
        f"Enter Category.\n(Food, Travel, Misc, Entertainment): ",
        lambda x: utils.validate_category(x.lower()),
        "Enter Valid Category.")).lower()
    description = input("Enter Description,(Press Enter if not): ")
    data_manager.add_new_exp(amount, category, description)


def display_all_expenses():
    expenses = data_manager.load_data()
    print("\n=== All Expenses ===")
    for doc in expenses:
        print(f"""
Transaction ID: {doc.get('id')}
Date          : {doc.get('date')}
Amount        : ₹{doc.get('amount')}
Category      : {doc.get('category')}
Description   : {doc.get('description') or 'N/A'}
-------------------------------""")


#Edit an expense entry
def edit_exp():
    try:
        target_id = input("Enter Expense Id To Edit: ").strip()
        id_list = [e.get("id") for e in expenses]
        if target_id in id_list:
            print("Enter Details To Update entry."
                  "\nClick Enter If You Don't Want To Change.")

            while True:
                date = input("Enter New Date: ").strip()
                if date and not utils.validate_date(date):
                    print("enter valid date")
                else:
                    break

            while True:
                amount = input("Enter New Amount: ").strip()
                if amount and not utils.validate_amount(amount):
                    print("Enter valid positive number")
                else:
                    break

            while True:
                category = input("Enter New Category."
                                 "\n (Food,Travel,Misc,Entertainment): "
                                 ).strip().lower()
                if category and not utils.validate_category(category):
                    print("Enter valid Category")
                else:
                    break

            description = input("Enter New Description: ")

            if data_manager.edit_expense(target_id,date,amount,category,description):
                print(f"Expense Entry ID: {target_id} Updated Successfully.")

                #Option to verify,whether it got updated
                user_assurance = input("Do You Want To See The Update(Y/N): ").lower()
                if user_assurance == "y":
                    reloaded_expense = data_manager.load_data()
                    updated_exp = [exp for exp in reloaded_expense if exp.get("id") == target_id]
                    print(updated_exp)
                else:
                    print("Thank You.")
            else:
                print(f"Nothing Changed in the ID:{target_id}")

        else:
            print(f"There is No Expense Entry with ID:{target_id}")

    except Exception as e:
        print(f"Error is: {e}")


#delete an expense entry
def delete_entry():
    removable_id = str(input(
        "Enter the id to remove the expense: "
    ).strip())
    if data_manager.delete_expense(removable_id):
        print(f"Expense Entry Deletion Successful."
              f"\n ID No: {removable_id} ")

    # user verifying the deletion
    see_update = input("Do you want to see the Updated expense List (y/n): ")
    if see_update.lower() == "y":
        updated_expense = data_manager.load_data()
        for doc in updated_expense:
            print(doc)

#filter expense by category
def filtered_category():
    #validating user entered category then passing to the function

    category = str(
        utils.validate_input("Enter Category."
                             "\n(Food,Travel,Misc,Entertainment): ",
                             utils.validate_category,
                             "Enter Valid Category!")).lower()

    reporter.filter_by_category(category)

#filter by date range
def filtered_date():
    #validating user entered start and end date and then passing them to the function

    start_date = utils.validate_input(
        "Start Date: ",utils.validate_date,
        "Enter Valid Date").strip()
    end_date = utils.validate_input(
        "End Date: ", utils.validate_date,
        "Enter Valid Date").strip()

    reporter.filter_by_date(start_date,end_date)

#summarize by month
def summarize_monthly():
    print("Expense Month Wise Summery")
    print("-" * 50)
    summary = reporter.summarize_by_month()

    for key, value in summary.items():
        print(f"Expense in Month {key} is: {value}")
    print(f"The Grand Total is: {reporter.total_expense(expenses)}")

#summerize by category
def summarize_category():
    print("Expense Category Wise Summery")
    print("-" * 50)
    summary = reporter.summarize_by_category()

    for key, value in summary.items():
        print(f"Total Expense in {key} is: {value}")
    print(f"The Grand Total is: {reporter.total_expense(expenses)}")

#import summaries into csv file
def export_to_csv(summary, file_name,head):
    file_path = os.path.join("Exported summaries", file_name)

    with open(file_path, "w", newline='') as file:
        writer = csv.writer(file)
        writer.writerow([head, "Total Amount"])
        for key, total in summary.items():
            writer.writerow([key, total])

def import_to_csv():
    print("How Do You Want To Import Summaries Into Csv")
    choice = int(input("1: Monthly Summary, 2: Categorical Summary : "))

    if choice == 1:
        summary = reporter.summarize_by_month()
        file_name = input("Enter File Name To Save: ").strip()
        if not file_name.endswith(".csv"):
            file_name += ".csv"
        try:
            export_to_csv(summary,file_name,"Months")
            print(f"Monthly Summery Saved Into: {file_name}")
        except Exception as e:
            print(f"Error occurred: {e}")

    elif choice == 2:
        summary = reporter.summarize_by_category()
        file_name = input("Enter File Name To Save: ").strip()
        if not file_name.endswith(".csv"):
            file_name += ".csv"
        try:
            export_to_csv(summary, file_name,"Category")
            print(f"Monthly Summery Saved Into: {file_name}")
        except Exception as e:
            print(f"Error occurred: {e}")

    else:
        print("invalid option!")
        return

#Main loop for menu
def main_loop():
    while True:
        #showing options and taking user input.
        try:
            print_menu()
            choose = int(input("Choose an option: "))

            #Exit the loop
            if choose == 0:
                break

            #Add new expense
            elif choose == 1:
                add_entry()

            #View all expenses
            elif choose == 2:
               display_all_expenses()
               break

            #Filter Expense By Date Range
            elif choose == 3:
                filtered_date()

            #Filter Expense By Category
            elif choose == 4:
                filtered_category()

            #edit an expense
            elif choose == 5:
                edit_exp()

            #Delete an expense
            elif choose == 6:
                delete_entry()
                break

            #show monthly summery
            elif choose == 7:
                summarize_monthly()

            #show category wise summery
            elif choose == 8:
                summarize_category()

            #export expenses into csv file
            elif choose == 9:
                import_to_csv()

            else:
                print("Invalid option. Please choose a valid menu item.")

        except ValueError:
            print("Enter valid Numerical Value!")


if __name__ == "__main__":
    main_loop()