import tkinter as tk
from tkinter import ttk, messagebox
from ttkthemes import ThemedStyle  # Import ThemedStyle from ttkthemes

import os

# Global variables
monthly_limit = 1000.00
daily_expenses = 0

def save_expense():
    global daily_expenses
    expense = entry_expense.get()
    amount = entry_amount.get()
    category = combo_category.get()

    if not expense or not amount or not category:
        messagebox.showerror("Error", "All fields are required.")
        return  

    try:
        amount = float(amount)
    except ValueError:
        messagebox.showerror("Error", "Amount must be a valid number.")
        return

    if daily_expenses + amount > monthly_limit:
        messagebox.showerror("Error", "Daily limit exceeded.")
        return

    with open("expenses.txt", "a") as file:
        file.write(f"Category: {category}, Expense: {expense}, Amount: {amount}\n")
    
    entry_expense.delete(0, tk.END)
    entry_amount.delete(0, tk.END)
    daily_expenses += amount
    update_daily_limit_label()
    messagebox.showinfo("Expense Tracker", "Expense saved successfully.")

def show_expenses():
    expenses_window = tk.Toplevel(root)
    expenses_window.title("Expenses")

    with open("expenses.txt", "r") as file: 
        expenses = file.readlines()

    expenses_text = tk.Text(expenses_window)
    expenses_text.pack() 

    for expense in expenses:
        expenses_text.insert(tk.END, expense)

def update_daily_limit_label():
    daily_limit_label.config(text=f"Daily Limit: {monthly_limit - daily_expenses:.2f} INR")

def reset_data():
    global daily_expenses
    if os.path.exists("expenses.txt"):
        os.remove("expenses.txt")
        daily_expenses = 0
        update_daily_limit_label()
        messagebox.showinfo("Expense Tracker", "All data has been reset.")
    else:
        messagebox.showinfo("Expense Tracker", "No data found to reset.")

root = tk.Tk() 
root.title("Expense Tracker")

# Create a themed style for the entire GUI
style = ThemedStyle(root)
style.set_theme("plastik")  # Choose your preferred theme, e.g., "plastik"

# Customize the main window's appearance
root.geometry("800x400")
root.configure(bg=style.lookup("TLabel", "background"))

# Create labels and entry fields for expense, amount, and category
label_expense = ttk.Label(root, text="Expense:")
label_expense.grid(row=0, column=0, padx=10, pady=10, sticky="w")
entry_expense = ttk.Entry(root)
entry_expense.grid(row=0, column=1, padx=10, pady=10)

label_amount = ttk.Label(root, text="Amount (INR):")
label_amount.grid(row=1, column=0, padx=10, pady=10, sticky="w")
entry_amount = ttk.Entry(root)
entry_amount.grid(row=1, column=1, padx=10, pady=10) 

label_category = ttk.Label(root, text="Category:")
label_category.grid(row=2, column=0, padx=10, pady=10, sticky="w")
categories = ["Food", "Transport", "Entertainment", "Shopping", "Other"]
combo_category = ttk.Combobox(root, values=categories)
combo_category.grid(row=2, column=1, padx=10, pady=10)
combo_category.set(categories[0])

button_save = ttk.Button(root, text="Save Expense", command=save_expense)
button_save.grid(row=3, column=1, padx=10, pady=10)

# Create the display tab
display_tab = ttk.Frame(root)
display_tab.grid(row=0, column=2, rowspan=4, padx=10, pady=10, sticky="n")

daily_limit_label = ttk.Label(display_tab, text="Daily Limit: 0.00 INR")  
daily_limit_label.pack(pady=10)
update_daily_limit_label()

button_show = ttk.Button(display_tab, text="Show Expenses", command=show_expenses)
button_show.pack(pady=10)

# Create a button to reset all data
button_reset_data = ttk.Button(display_tab, text="Reset Data", command=reset_data)
button_reset_data.pack(pady=10)

if not os.path.exists("expenses.txt"):
    with open("expenses.txt", "w"):
        pass

root.mainloop()
 