import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from datetime import datetime

FILE_NAME = "expenses.json"

class ExpenseTracker:
    def __init__(self, root):
        self.root = root
        self.root.title("Expense Tracker")
        self.root.geometry("650x600")

        self.expenses = self.load_data()

        # --- Форма ввода ---
        input_frame = tk.LabelFrame(root, text="Добавить расход", padx=10, pady=10)
        input_frame.pack(fill="x", padx=10, pady=5)

        tk.Label(input_frame, text="Сумма:").grid(row=0, column=0)
        self.amount_entry = tk.Entry(input_frame)
        self.amount_entry.grid(row=0, column=1, padx=5)

        tk.Label(input_frame, text="Категория:").grid(row=0, column=2)
        self.category_cb = ttk.Combobox(input_frame, values=["Еда", "Транспорт", "Развлечения", "Жилье", "Прочее"])
        self.category_cb.grid(row=0, column=3, padx=5)

        tk.Label(input_frame, text="Дата (ГГГГ-ММ-ДД):").grid(row=1, column=0, pady=5)
        self.date_entry = tk.Entry(input_frame)
        self.date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))
        self.date_entry.grid(row=1, column=1, padx=5)

        tk.Button(input_frame, text="Добавить расход", command=self.add_expense, bg="green", fg="white").grid(row=1, column=3, sticky="we")

        # --- Фильтры ---
        filter_frame = tk.LabelFrame(root, text="Фильтрация и Итоги", padx=10, pady=10)
        filter_frame.pack(fill="x", padx=10, pady=5)

        tk.Label(filter_frame, text="Категория:").grid(row=0, column=0)
        self.filter_cat = ttk.Combobox(filter_frame, values=["Все"] + ["Еда", "Транспорт", "Развлечения", "Жилье", "Прочее"])
        self.filter_cat.current(0)
        self.filter_cat.grid(row=0, column=1, padx=5)

        tk.Button(filter_frame, text="Применить фильтр", command=self.refresh_table).grid(row=0, column=2, padx=5)
        self.total_label = tk.Label(filter_frame, text="Итого: 0", font=("Arial", 10, "bold"))
        self.total_label.grid(row=0, column=3, padx=20)

        # --- Таблица ---
        self.tree = ttk.Treeview(root, columns=("Дата", "Категория", "Сумма"), show="headings")
        self.tree.heading("Дата", text="Дата")
        self.tree.heading("Категория", text="Категория")
        self.tree.heading("Сумма", text="Сумма")
        self.tree.pack(fill="both", expand=True, padx=10, pady=5)

        self.refresh_table()

    def load_data(self):
        if os.path.exists(FILE_NAME):
            with open(FILE_NAME, "r", encoding="utf-8") as f:
                return json.load(f)
        return []

    def save_data(self):
        with open(FILE_NAME, "w", encoding="utf-8") as f:
            json.dump(self.expenses, f, indent=4, ensure_ascii=False)

    def validate_date(self, date_text):
        try:
            datetime.strptime(date_text, '%Y-%m-%d')
            return True
        except ValueError:
            return False

    def add_expense(self):
        try:
            amount = float(self.amount_entry.get())
            if amount <= 0: raise ValueError
        except ValueError:
            messagebox.showerror("Ошибка", "Сумма должна быть положительным числом!")
            return

        date = self.date_entry.get()
        if not self.validate_date(date):
            messagebox.showerror("Ошибка", "Формат даты: ГГГГ-ММ-ДД")
            return

        category = self.category_cb.get()
        if not category:
            messagebox.showerror("Ошибка", "Выберите категорию!")
            return

        self.expenses.append({"date": date, "category": category, "amount": amount})
        self.save_data()
        self.refresh_table()
        self.amount_entry.delete(0, tk.END)

    def refresh_table(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        selected_cat = self.filter_cat.get()
        total = 0

        for exp in sorted(self.expenses, key=lambda x: x['date'], reverse=True):
            if selected_cat == "Все" or exp['category'] == selected_cat:
                self.tree.insert("", tk.END, values=(exp['date'], exp['category'], f"{exp['amount']:.2f}"))
                total += exp['amount']

        self.total_label.config(text=f"Итого: {total:.2f}")

if __name__ == "__main__":
    root = tk.Tk()
    app = ExpenseTracker(root)
    root.mainloop()
