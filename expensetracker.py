from expense import Expense
from db import get_connection
import calendar
import datetime


def add_expense_to_db(expense):
    conn = get_connection()
    cursor = conn.cursor()
    query = "INSERT INTO expenses (name, amount, category, date) VALUES (%s, %s, %s, %s)"
    today = datetime.date.today()
    cursor.execute(query, (expense.name, expense.amount, expense.category, today))
    conn.commit()
    cursor.close()
    conn.close()

def fetch_all_expenses():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, amount, category, date FROM expenses ORDER BY date DESC")
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows

def main():
    budget = 2000
    while True:
        print("\n=== Expense Tracker Menu ===")
        print("1. Add Expense")
        print("2. View Expenses")
        print("3. Exit")
        choice = input("Enter your choice: ").strip()

        if choice == "1":
            expense = get_user_expense()
            add_expense_to_db(expense)
            print(" Expense added to database.")
            summarize_expenses(budget)

        elif choice == "2":
            view_expenses()

        elif choice == "3":
            print("Goodbye!")
            break

        else:
            print("Invalid choice, please try again.")

def get_user_expense():
    print("\n Getting User Expense")
    expense_name = input("Enter expense name: ")
    expense_amount = float(input("Enter expense amount: "))
    expense_categories = [
        " Food",
        "Home",
        " Work",
        " Fun",
        " Misc",
    ]

    while True:
        print("Select a category: ")
        for i, category_name in enumerate(expense_categories):
            print(f"  {i + 1}. {category_name}")

        value_range = f"[1 - {len(expense_categories)}]"
        selected_index = int(input(f"Enter a category number {value_range}: ")) - 1

        if selected_index in range(len(expense_categories)):
            selected_category = expense_categories[selected_index]
            new_expense = Expense(
                name=expense_name, category=selected_category, amount=expense_amount
            )
            return new_expense
        else:
            print("Invalid category. Please try again!")

def summarize_expenses(budget):
    rows = fetch_all_expenses()
    expenses = []
    for r in rows:
        _, name, amount, category, date = r
        expenses.append(Expense(name=name, category=category, amount=float(amount)))

    amount_by_category = {}
    for expense in expenses:
        key = expense.category
        amount_by_category[key] = amount_by_category.get(key, 0.0) + expense.amount

    print("\nExpenses By Category 📈:")
    if amount_by_category:
        for key, amount in amount_by_category.items():
            print(f"  {key}: Rs{amount:.2f}")
    else:
        print("  No expenses found.")

    total_spent = sum([x.amount for x in expenses])
    print(f"\nTotal Spent: Rs:{total_spent:.2f}")

    remaining_budget = budget - total_spent
    print(f" Budget Remaining: Rs:{remaining_budget:.2f}")

    now = datetime.datetime.now()
    days_in_month = calendar.monthrange(now.year, now.month)[1]
    remaining_days = days_in_month - now.day

    if remaining_days <= 0:
        print(green(" No remaining days left in this month to compute daily budget."))
    else:
        daily_budget = remaining_budget / remaining_days
        print(green(f" Budget Per Day: Rs:{daily_budget:.2f}"))

def view_expenses():
    rows = fetch_all_expenses()
    if not rows:
        print("\n No expenses recorded yet.")
        return
    print("\n=== All Expenses ===")
    print(f"{'ID':<5}{'Date':<12}{'Category':<12}{'Amount':<10}{'Name'}")
    print("-" * 50)
    for exp_id, name, amount, category, date in rows:
        print(f"{exp_id:<5}{date:<12}{category:<12}{amount:<10}{name}")

def green(text):
    return f"\033[92m{text}\033[0m"

if __name__ == "__main__":
    main()
