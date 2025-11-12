import tkinter as tk
from tkinter import ttk, messagebox

# ---------------------- Data ----------------------
products = [
    {"name": "Laptop", "price": 55000},
    {"name": "Headphones", "price": 2500},
    {"name": "Keyboard", "price": 1500},
    {"name": "Mouse", "price": 800},
    {"name": "Smartphone", "price": 22000},
    {"name": "Charger", "price": 600}
]

cart = []

# ---------------------- Functions ----------------------
def add_to_cart(product):
    cart.append(product)
    update_cart()

def remove_selected():
    selected = cart_box.curselection()
    if not selected:
        messagebox.showwarning("No item", "Please select an item to remove.")
        return
    index = selected[0]
    cart.pop(index)
    update_cart()

def clear_cart():
    if not cart:
        messagebox.showinfo("Cart Empty", "Nothing to clear.")
        return
    if messagebox.askyesno("Clear Cart", "Are you sure you want to remove all items?"):
        cart.clear()
        update_cart()

def update_cart():
    cart_box.delete(0, tk.END)
    total = 0
    for item in cart:
        cart_box.insert(tk.END, f"{item['name']} - ₹{item['price']}")
        total += item['price']
    total_label.config(text=f"Total: ₹{total}")

def checkout():
    if not cart:
        messagebox.showinfo("Empty Cart", "Add items to the cart first.")
        return
    total = sum(item['price'] for item in cart)
    messagebox.showinfo("Checkout", f"Purchase successful!\nTotal Amount: ₹{total}")
    cart.clear()
    update_cart()

# ---------------------- GUI ----------------------
root = tk.Tk()
root.title("E-Commerce Cart")
root.geometry("600x450")
root.config(bg="#F5F5F5")

title = tk.Label(root, text="🛒 E-Commerce Cart", font=("Arial", 18, "bold"), bg="#F5F5F5", fg="#333")
title.pack(pady=10)

# Product List
frame_left = tk.Frame(root, bg="#F5F5F5")
frame_left.pack(side="left", fill="y", padx=20)

tk.Label(frame_left, text="Available Products", font=("Arial", 12, "bold"), bg="#F5F5F5").pack()

for product in products:
    frame_item = tk.Frame(frame_left, bg="#F5F5F5")
    frame_item.pack(fill="x", pady=2)
    tk.Label(frame_item, text=f"{product['name']} - ₹{product['price']}", bg="#F5F5F5").pack(side="left")
    tk.Button(frame_item, text="Add", bg="#4CAF50", fg="white",
              command=lambda p=product: add_to_cart(p)).pack(side="right", padx=5)

# Cart Section
frame_right = tk.Frame(root, bg="#F5F5F5")
frame_right.pack(side="right", fill="both", expand=True, padx=20)

tk.Label(frame_right, text="Your Cart", font=("Arial", 12, "bold"), bg="#F5F5F5").pack()
cart_box = tk.Listbox(frame_right, height=10, width=35, font=("Arial", 11))
cart_box.pack(pady=5)

total_label = tk.Label(frame_right, text="Total: ₹0", font=("Arial", 12, "bold"), bg="#F5F5F5", fg="#333")
total_label.pack(pady=5)

button_frame = tk.Frame(frame_right, bg="#F5F5F5")
button_frame.pack(pady=10)

tk.Button(button_frame, text="Remove Selected", bg="#FF7043", fg="white",
          command=remove_selected).grid(row=0, column=0, padx=5)
tk.Button(button_frame, text="Clear Cart", bg="#E53935", fg="white",
          command=clear_cart).grid(row=0, column=1, padx=5)
tk.Button(button_frame, text="Checkout", bg="#1E88E5", fg="white",
          command=checkout).grid(row=0, column=2, padx=5)

root.mainloop()
