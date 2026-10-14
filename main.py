import tkinter as tk
from tkinter import ttk

# This is the default window size and title of the window. 
root = tk.Tk()
root.title("Nosh & Nibbles -  Shopping List")
root.geometry("1000x400") 
root.resizable(True, True) #True allows resizing of Length and Width, False disables resizing
root.columnconfigure(0, weight=1) #weight=1 allows the column to expand when the window is resized
root.rowconfigure(0, weight=1) #weight=1 allows the row to expand when the window is resized


#FRAMES: The following code creates frames for the window. Frames are used to group widgets together. 
content = ttk.Frame(root, padding = 15)
entry_frame = ttk.LabelFrame(content, text="Enter Item:", padding=10)
cart_frame = ttk.LabelFrame(content, text="Shopping Cart", padding=10)
control_frame = ttk.Frame(content, padding=10)


# WIDGETS: The following code creates widgets for the window.

#Buttons for the entry_frame and control_frame
add_item = ttk.Button(entry_frame, text="Add Item")
remove_item = ttk.Button(entry_frame, text="Remove Item")
clear_cart = ttk.Button(control_frame, text="Clear Cart")

# Item entry field for the entry_frame
item_label = ttk.Label(entry_frame, text="Item Name:")
item_entry = ttk.Entry(entry_frame, width=30)

quantity_label = ttk.Label(entry_frame, text="Quantity:")
quantity_entry = ttk.Entry(entry_frame, width=30)

category_label = ttk.Label(entry_frame, text="Category:")
category_entry = ttk.Combobox(
    entry_frame, values=["Produce", "Dairy", "Meat", "Bakery", "Pantry", "Frozen", "Beverages"],
    state="readonly", width=27)

# Shopping cart listbox for the cart_frame
cart_listbox = ttk.Treeview(cart_frame, columns=("Item", "Quantity", "Category"), show="headings", height=10)
cart_listbox.heading("Item", text="Item")
cart_listbox.heading("Quantity", text="Quantity")
cart_listbox.heading("Category", text="Category")


#LAYOUT: The following code positions the frames and widgets in the window

#Frames are positioned in the window using the grid layout manager. 
content.grid(column=0, row=0, stick="nsew") # stiocky="nsew" allows the frame to expand in all directions
entry_frame.grid(column=0, row=0, padx=10, pady=10, sticky="nsew")#"n" aligns a widget to the top of the frame
cart_frame.grid(column=1, row=0, padx=10, pady=10, sticky="nsew")
control_frame.grid(column=0, row=1, columnspan=2, padx=10, pady=10)#control frame acts as container for other widgets and frames. 

#This section of code positions the widgets in the window
add_item.grid(column=0, row=3, padx=5, pady=5)
remove_item.grid(column=1, row=3, padx=5, pady=5)
clear_cart.grid(column=0, row=0, padx=5, pady=5)

item_label.grid(column=0, row=0, padx=5, pady=5, sticky="w")
item_entry.grid(column=1, row=0, padx=5, pady=5)

quantity_label.grid(column=0, row=1, padx=5, pady=5, sticky="w")
quantity_entry.grid(column=1, row=1, padx=5, pady=5)

#Combobox for category selection is positioned in the entry_frame
category_label.grid(column=0, row=2, padx=5, pady=5, sticky="w")
category_entry.grid(column=1, row=2, padx=5, pady=5)

#The shopping cart listbox is positioned in the cart_frame
cart_listbox.grid(column=0, row=0, padx=5, pady=5, sticky="nsew")

root.mainloop()