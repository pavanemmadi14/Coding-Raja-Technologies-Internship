import tkinter as tk
from tkinter import messagebox, simpledialog
import json
import os

class Transaction:
    def __init__(self, type, category, amount):
        self.type = type  # 'income' or 'expense'
        self.category = category
        self.amount = amount

    def to_dict(self):
        return {
            'type': self.type,
            'category': self.category,
            'amount': self.amount
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            type=data['type'],
            category=data['category'],
            amount=data['amount']
        )

class BudgetTracker:
    def __init__(self, filename='transactions.json'):
        self.transactions = []
        self.filename = filename
        self.load_transactions()

    def add_transaction(self, type, category, amount):
        transaction = Transaction(type, category, amount)
        self.transactions.append(transaction)
        self.save_transactions()

    def calculate_budget(self):
        income = sum(t.amount for t in self.transactions if t.type == 'income')
        expenses = sum(t.amount for t in self.transactions if t.type == 'expense')
        return income - expenses

    def analyze_expenses(self):
        categories = {}
        for transaction in self.transactions:
            if transaction.type == 'expense':
                if transaction.category in categories:
                    categories[transaction.category] += transaction.amount
                else:
                    categories[transaction.category] = transaction.amount
        return categories

    def save_transactions(self):
        with open(self.filename, 'w') as file:
            json.dump([transaction.to_dict() for transaction in self.transactions], file, indent=4)

    def load_transactions(self):
        if os.path.exists(self.filename):
            with open(self.filename, 'r') as file:
                transactions_data = json.load(file)
                self.transactions = [Transaction.from_dict(data) for data in transactions_data]

class BudgetTrackerGUI(tk.Tk):
    def __init__(self, tracker):
        super().__init__()
        self.tracker = tracker
        self.title("Budget Tracker")
        self.geometry("600x400")

        self.create_widgets()

    def create_widgets(self):
        self.listbox = tk.Listbox(self, height=15, width=60)
        self.listbox.pack(pady=20)

        self.add_income_button = tk.Button(self, text="Add Income", command=self.add_income)
        self.add_income_button.pack(pady=5)

        self.add_expense_button = tk.Button(self, text="Add Expense", command=self.add_expense)
        self.add_expense_button.pack(pady=5)

        self.calculate_budget_button = tk.Button(self, text="Calculate Budget", command=self.calculate_budget)
        self.calculate_budget_button.pack(pady=5)

        self.analyze_expenses_button = tk.Button(self, text="Analyze Expenses", command=self.analyze_expenses)
        self.analyze_expenses_button.pack(pady=5)

        self.update_transaction_list()

    def update_transaction_list(self):
        self.listbox.delete(0, tk.END)
        for transaction in self.tracker.transactions:
            self.listbox.insert(tk.END, f"{transaction.type.capitalize()} - {transaction.category}: {transaction.amount}")

    def add_income(self):
        category = simpledialog.askstring("Income Category", "Enter income category:")
        amount = simpledialog.askfloat("Income Amount", "Enter income amount:")
        if category and amount:
            self.tracker.add_transaction('income', category, amount)
            self.update_transaction_list()

    def add_expense(self):
        category = simpledialog.askstring("Expense Category", "Enter expense category:")
        amount = simpledialog.askfloat("Expense Amount", "Enter expense amount:")
        if category and amount:
            self.tracker.add_transaction('expense', category, amount)
            self.update_transaction_list()

    def calculate_budget(self):
        budget = self.tracker.calculate_budget()
        messagebox.showinfo("Budget", f"Remaining budget: {budget}")

    def analyze_expenses(self):
        expenses = self.tracker.analyze_expenses()
        analysis = "\n".join(f"{category}: {amount}" for category, amount in expenses.items())
        messagebox.showinfo("Expense Analysis", f"Expenses by category:\n{analysis}")

if __name__ == "__main__":
    tracker = BudgetTracker()
    app = BudgetTrackerGUI(tracker)
    app.mainloop()
