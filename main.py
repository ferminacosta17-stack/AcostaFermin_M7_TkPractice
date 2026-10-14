import tkinter as tk
from tkinter import ttk
from tkinter import messagebox #added to display warning messages when the user does not fill in all fields or does not select an item to remove.

#----------------------------------------------------------------------------#

# This is the default window size and title of the window and restraints
root = tk.Tk()
root.title("Nosh & Nibbles - Shopping List")
root.geometry("1000x400")
root.minsize(800, 300) #minimum size of the window when resized
root.resizable(True, True) #True allows resizing of Length and Width, False disables resizing
root.columnconfigure(0, weight=1) #weight=1 allows the column to expand when the window is resized
root.rowconfigure(0, weight=1) #weight=1 allows the row to expand when the window is resized


#--------------------------------------------------------------------------#

#FRAMES: The following code creates frames for the window. Frames are used to group widgets together. 
content = ttk.Frame(root, padding = 15)
entry_frame = ttk.LabelFrame(content, text="Enter Item:", padding=10)
cart_frame = ttk.LabelFrame(content, text="Shopping Cart", padding=10)
control_frame = ttk.Frame(content, padding=10)
# The following code configures the grid layout for the frames.
content.columnconfigure(1, weight=1)
content.rowconfigure(0, weight=1)
cart_frame.columnconfigure(0, weight=1)
cart_frame.rowconfigure(0, weight=1)

#--------------------------------------------------------------------------#

#DEFINE COMMANDS: The following code defines the functions that will be called when the buttons are clicked.

#defining add item logic and input validation 
def add_item_to_cart():
    item = item_entry.get().strip()#.strip() removes any leading or trailing whitespace from the input.
    quantity = quantity_entry.get()
    category = category_entry.get()

    if item and quantity and category: #if not handles input validation.
        
        if not quantity.isdigit() or int(quantity) <= 0:
            tk.messagebox.showwarning("Input Error", "Quantity must be a positive integer.")
            return
        
        if not item.replace(" ", "").isalpha(): #input validation for item name to be alphanumeric.
            tk.messagebox.showwarning("Input Error", "Item name must be alphabetic.")
            return
        
        cart_list.insert("", "end", values=(item, quantity, category))
        update_item_count() #update the item counter in the shopping cart frame after adding an item
        item_entry.delete(0, "end")
        quantity_entry.delete(0, "end")
        category_entry.set("")
   
    else:
        tk.messagebox.showwarning("Input Error", "Please fill in all fields.")

#defning remove item logic and input validation
def remove_item_from_cart():
    selected_items = cart_list.selection()
    if selected_items:
        for item in selected_items:
            cart_list.delete(item)
        update_item_count() #update the item counter after removing an item
    else:
        tk.messagebox.showwarning("Selection Error", "Please select an item to remove.")

#defining clear cart logic
def clear_shopping_cart():
    for item in cart_list.get_children():
        cart_list.delete(item)
    update_item_count() #update the item counter after removing all items

#defning function to update the item counter in the shopping cart frame
def update_item_count():
    unique_items = len(cart_list.get_children())
    total_items = sum(int(cart_list.item(item, "values")[1]) for item in cart_list.get_children())

    item_count_label.config(text=f"Total Items: {unique_items}")
    total_quantity_label.config(text=f"Total Quantity: {total_items}")

#--------------------------------------------------------------------------#

#MENU BAR: The following code creates a menu bar for the window. The menu bar will contain an order menu with an Exit option.

menu_bar = tk.Menu(root)
order_menu = tk.Menu(menu_bar, tearoff=0) #tearoff=0 removes the dashed line at the top of the menu
menu_bar.add_cascade(label="File", menu=order_menu)
order_menu.add_command(label="Create Order", command=clear_shopping_cart) #command=clear_shopping_cart clears the shopping cart when the user clicks on Create Order
order_menu.add_command(label="Exit", command=root.quit) #command=root.quit closes the window
root.config(menu=menu_bar)

#--------------------------------------------------------------------------#

# WIDGETS: The following code creates widgets for the window.

#Buttons to interact with each frame.
add_item = ttk.Button(entry_frame, text="Add Item", command=add_item_to_cart)
remove_item = ttk.Button(cart_frame, text="Remove Item", command=remove_item_from_cart)
clear_cart = ttk.Button(cart_frame, text="Clear Cart", command=clear_shopping_cart)

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
cart_list = ttk.Treeview(cart_frame, columns=("Item", "Quantity", "Category"), show="headings", height=10)
cart_list.heading("Item", text="Item")
cart_list.heading("Quantity", text="Quantity")
cart_list.heading("Category", text="Category")
#Addtional configuration for the listbox to allow for resizing and scrolling
cart_list.column("Item", width=150, minwidth=80, stretch=True, anchor="w") #anchoring help align in the column
cart_list.column("Quantity", width=100, minwidth=60, stretch=True, anchor="center")
cart_list.column("Category", width=150, minwidth=80, stretch=True, anchor="center")

#Adding a item counter in the shopping cart frame to display the number of items in the cart
item_count_label = ttk.Label(cart_frame, text="Total Items: 0")
total_quantity_label = ttk.Label(cart_frame, text="Total Quantity: 0")

#--------------------------------------------------------------------------#

#LAYOUT: The following code positions the frames and widgets in the window

#Frames are positioned in the window using the grid layout manager. 
content.grid(column=0, row=0, sticky="nsew") # sticky="nsew" allows the frame to expand in all directions
entry_frame.grid(column=0, row=0, padx=10, pady=10, sticky="nsew")#"n" aligns a widget to the top of the frame
cart_frame.grid(column=1, row=0, padx=10, pady=10, sticky="nsew")
control_frame.grid(column=0, row=1, columnspan=2, padx=10, pady=10)#control frame acts as container for other widgets and frames. 

#This section of code positions the widgets in the window
add_item.grid(column=1, row=3, padx=5, pady=5)
remove_item.grid(column=0, row=3, padx=5, pady=5)
clear_cart.grid(column=1, row=3, padx=5, pady=5)

item_label.grid(column=0, row=0, padx=5, pady=5, sticky="w")
item_entry.grid(column=1, row=0, padx=5, pady=5)

quantity_label.grid(column=0, row=1, padx=5, pady=5, sticky="w")
quantity_entry.grid(column=1, row=1, padx=5, pady=5)

#Combobox for category selection is positioned in the entry_frame
category_label.grid(column=0, row=2, padx=5, pady=5, sticky="w")
category_entry.grid(column=1, row=2, padx=5, pady=5)

#The shopping cart listbox is positioned in the cart_frame
cart_list.grid(column=0, row=0, padx=5, pady=5, sticky="nsew")
#The item counter label is positioned in the bottom left of cart_frame
item_count_label.grid(column=0, row=1, padx=5, pady=5, sticky="w")
#Total quanity label is positioned in the bottom right of cart_frame
total_quantity_label.grid(column=1, row=1, padx=5, pady=5, sticky="e")

root.mainloop()