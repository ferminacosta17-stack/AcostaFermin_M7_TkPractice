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

#FRAME LAYOUT: The following code creates frames for the window. Frames are used to group widgets together. 
content = ttk.Frame(root, padding = 15)
entry_frame = ttk.LabelFrame(content, text="Enter Item:", padding=10)
cart_frame = ttk.LabelFrame(content, text="Shopping Cart", padding=10)

#Adjusted the positions of Remove, Edit, Clear buttons in the cart_frame to be in a single row and aligned to the right of the frame.
cart_button_frame = ttk.Frame(cart_frame)

#Created an additional frame to position counters to the edge of cart_frame.
counter_frame = ttk.Frame(cart_frame)

# The following code configures the grid layout for the frames.
content.columnconfigure(1, weight=1)
content.rowconfigure(0, weight=1)
cart_frame.columnconfigure(0, weight=1)
cart_frame.rowconfigure(0, weight=1)

#--------------------------------------------------------------------------#

#DEFINE COMMANDS: The following code defines the functions that will be called when the buttons are clicked.

#Defining add item logic and input validation 
def add_item_to_cart():
    item = item_entry.get().strip()#.strip() removes any leading or trailing whitespace from the input.
    quantity = quantity_entry.get()
    category = category_entry.get()

    if item and quantity and category: #if not handles input validation.
        
        if not quantity.isdigit() or int(quantity) <= 0: #validates quantity
            tk.messagebox.showwarning("Input Error", "Quantity must be a positive integer.")
            return
        
        if not item.replace(" ", "").isalpha(): #validates name
            tk.messagebox.showwarning("Input Error", "Item name must be alphabetic.")
            return

        for row in cart_list.get_children():# Added line to check for duplicate items
            existing_item = cart_list.item(row, "values")[0]
            if item.casefold() == existing_item.casefold():
                confirm = tk.messagebox.askyesno( 
                "Entry Already Exists", f"{item} is already in your shopping cart.\n"
                "Would you like to edit the existing entry?")

                if confirm: 
                    cart_list.selection_set(row)
                    cart_list.focus(row)
                    edit_item_in_cart()
                return
        #Adds items to cart
        cart_list.insert("", "end", values=(item, quantity, category))
        update_item_count() #update the item counter in the shopping cart frame after adding an item
    
        item_entry.delete(0, "end")
        quantity_entry.delete(0, "end")
        category_entry.set("")

    else:
        tk.messagebox.showwarning("Input Error", "Please fill in all fields.")

#Defining remove item logic and input validation
def remove_item_from_cart():
    selected_items = cart_list.selection()
    if selected_items:
        for item in selected_items:
            cart_list.delete(item)

        update_item_count() #update the item counter after removing an item
    else:
        tk.messagebox.showwarning("Selection Error", "Please select an item to remove.")

#Defining clear cart logic
#Modified function, asks users to confirm befor clearing. 
def clear_shopping_cart(confirm=True):
    if confirm and cart_list.get_children():
        if not tk.messagebox.askyesno(
            "Clear Cart",
            "Are you sure you want to clear the shopping cart?"
        ):
            return

    for item in cart_list.get_children():
        cart_list.delete(item)

    update_item_count() #update the item counter after removing all items


#Defining function to update the item counter in the shopping cart frame
def update_item_count():
    unique_items = len(cart_list.get_children())
    total_items = sum(int(cart_list.item(item, "values")[1]) for item in cart_list.get_children())

    item_count_label.config(text=f"Total Items: {unique_items}")
    total_quantity_label.config(text=f"Total Quantity: {total_items}")

#Optimizing the Create Order function to prompt user for confirmation before clearing the shopping cart.
def create_new_order():
    if cart_list.get_children():  # Check if the cart is not empty
        confirm = tk.messagebox.askyesno("Confirm New Order", "Are you sure you want to create a new order? This will clear the current shopping cart.")
        if confirm:
            clear_shopping_cart(confirm=False) #Added confirm=False to prevent a second confirmation
            item_entry.delete(0, "end")
            quantity_entry.delete(0, "end")
            category_entry.set("")

    else:
        tk.messagebox.showinfo("No Items", "The shopping cart is already empty.")

#Defining edit item logic and input validation
def edit_item_in_cart():
    selected_items = cart_list.selection()
    if selected_items:
        item_id = selected_items[0]
        item_values = cart_list.item(item_id, "values")
        
        # Pre-fill the entry fields with the selected item's values
        item_entry.delete(0, "end")
        item_entry.insert(0, item_values[0])
        
        quantity_entry.delete(0, "end")
        quantity_entry.insert(0, item_values[1])
        
        category_entry.set(item_values[2])
        
        # Remove the selected item from the cart
        cart_list.delete(item_id)

        update_item_count()  # Update the item counter after removing the item
    else:
        tk.messagebox.showwarning("Selection Error", "Please select an item to edit.")

#--------------------------------------------------------------------------#

#MENU BAR: The following code creates a menu bar for the window. The menu bar will contain an order menu with an Exit option.

menu_bar = tk.Menu(root)
order_menu = tk.Menu(menu_bar, tearoff=0) #tearoff=0 removes the dashed line at the top of the menu
menu_bar.add_cascade(label="File", menu=order_menu)
order_menu.add_command(label="Create Order", command=create_new_order) #command=create_new_order prompts user for confirmation before clearing the shopping cart
order_menu.add_command(label="Exit", command=root.destroy) #command=root.destroy Exits the application when the user clicks on Exit and destroys the window and all its widgets.
root.config(menu=menu_bar)

#--------------------------------------------------------------------------#

# WIDGETS: The following code creates widgets for the window.

#Buttons to interact with each frame.
add_item = ttk.Button(entry_frame, text="Add Item", command=add_item_to_cart)\

#Moved buttons to a frame called cart_button_frame to allow for better alignment and organization of the buttons in the cart_frame.
remove_item = ttk.Button(cart_button_frame, text="Remove Item", command=remove_item_from_cart)
clear_cart = ttk.Button(cart_button_frame, text="Clear Cart", command=clear_shopping_cart)

#Added an additional Edit Item button to allow the user to edit the selected item in the shopping cart. 
#The edit_item function is defined to handle the logic for editing an item.
edit_item = ttk.Button(cart_button_frame, text="Edit Item", command=edit_item_in_cart)

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

#Additional configuration for the listbox to allow for resizing and scrolling
cart_list.column("Item", width=150, minwidth=80, stretch=True, anchor="w") #anchoring help align in the column
cart_list.column("Quantity", width=100, minwidth=60, stretch=True, anchor="center")
cart_list.column("Category", width=150, minwidth=80, stretch=True, anchor="center")

#Adding an item counter in the shopping cart frame to display the number of items in the cart
item_count_label = ttk.Label(counter_frame, text="Total Items: 0") #moved counter to counter_frame
total_quantity_label = ttk.Label(counter_frame, text="Total Quantity: 0")

#--------------------------------------------------------------------------#

#GRID LAYOUT: The following code positions the frames and widgets in the window

#Frames are positioned in the window using the grid layout manager. 
content.grid(column=0, row=0, sticky="nsew") # sticky="nsew" allows the frame to expand in all directions
entry_frame.grid(column=0, row=0, padx=10, pady=10, sticky="nsew")#"n" aligns a widget to the top of the frame
cart_frame.grid(column=1, row=0, padx=10, pady=10, sticky="nsew")
cart_list.grid(column=0, row=0, padx=5, pady=5, sticky="nsew") #The shopping cart listbox is positioned in the cart_frame


#This section of code positions widgets in their respective frames
add_item.grid(column=1, row=3, padx=5, pady=5)

#Adjusted position of buttons in frame
remove_item.grid(column=0, row=0, padx=10, pady=5)
clear_cart.grid(column=2, row=0, padx=10, pady=5)
edit_item.grid(column=1, row=0, padx=10, pady=5) # added edit item button to the cart_frame to allow the user to edit the selected item in the shopping cart.

item_label.grid(column=0, row=0, padx=5, pady=5, sticky="w")
item_entry.grid(column=1, row=0, padx=5, pady=5)

quantity_label.grid(column=0, row=1, padx=5, pady=5, sticky="w")
quantity_entry.grid(column=1, row=1, padx=5, pady=5)

#Combobox for category selection is positioned in the entry_frame
category_label.grid(column=0, row=2, padx=5, pady=5, sticky="w")
category_entry.grid(column=1, row=2, padx=5, pady=5)

#Added positioning to the counter_frame.
counter_frame.grid(column=0, row=1, columnspan=2, sticky="ew", padx=5, pady=5)
counter_frame.columnconfigure(1, weight=1) #allows the item counter label to expand when the window is resized

#The item counter label is positioned in the bottom left of cart_frame
item_count_label.grid(column=0, row=1, padx=5, pady=5, sticky="w")
#Total quantity label is positioned in the bottom right of cart_frame
total_quantity_label.grid(column=1, row=1, padx=5, pady=5, sticky="e")

#Positions the cart_button_frame housing the Remove, Edit, Clear buttons.
cart_button_frame.grid(column=0, row=2, pady=10)

#--------------------------------------------------------------------------#
root.mainloop()