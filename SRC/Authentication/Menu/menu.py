import json
from tabulate import tabulate

def load_menu():
    """Load menu from a JSON file."""
    try:
        with open("menu.json", "r") as file:
            menu = json.load(file)
    except FileNotFoundError:
        menu = {
            "Breakfast": [],
            "Lunch": [],
            "Dinner": [],
            "Beverages": []
        }
    return menu

def display_menu(menu):
    """Display the full menu to the customer in tabular format."""
    print("\n--- Menu ---")
    for category in menu:
        print(f"\n{category} Menu:")
        table = []
        
        if not menu[category]:
            print("No items available.")
        else:
            count = 1  # Initialize counter
            for item in menu[category]:
                if 'item_price' in item:
                    row = [count, item['item_name'], f"{item['item_price']}", "N/A", "N/A"]
                elif 'half_plate_price' in item and 'full_plate_price' in item:
                    row = [count, item['item_name'], "N/A", f"{item['half_plate_price']}", f"{item['full_plate_price']}"]
                else:
                    row = [count, item['item_name'], "N/A", "N/A", "N/A"]
                
                table.append(row)
                count += 1  # Increment counter

            headers = ["Item No.", "Item Name", "Single Item", "Half Plate", "Full Plate"]
            print(tabulate(table, headers, tablefmt="grid"))

def add_menu_item():
    """Allow the admin to add an item to the menu."""
    menu = load_menu()

    print("\nSelect category to add item:")
    categories = list(menu.keys())
    
    count = 1  # Initialize counter
    for category in categories:
        print(f"{count}. {category}")
        count += 1  # Increment counter

    try:
        category_choice = int(input("Enter category number: ")) - 1
        if category_choice not in range(len(categories)):
            print("Invalid category selection.")
            return
        category = categories[category_choice]
    except ValueError:
        print("Invalid input. Please enter a number.")
        return

    item_name = input(f"Enter item name for {category}: ").strip()
    
    add_quantity = input("Do you want to add quantity options (half plate/full plate)? (y/n): ").strip().lower()

    if add_quantity == "y":
        while True:
            try:
                half_plate_price = float(input(f"Enter half plate price for {item_name}: "))
                full_plate_price = float(input(f"Enter full plate price for {item_name}: "))
                if half_plate_price < 0 or full_plate_price < 0:
                    print("Price can't be negative. Please enter valid prices.")
                    continue
                break
            except ValueError:
                print("Invalid price. Please enter valid numbers.")

        item = {
            "item_name": item_name,
            "half_plate_price": half_plate_price,
            "full_plate_price": full_plate_price
        }
        
    elif add_quantity == "n":
        while True:
            try:
                item_price = float(input(f"Enter price for {item_name}: "))
                if item_price < 0:
                    print("Price can't be negative. Please enter a valid price.")
                    continue
                break
            except ValueError:
                print("Invalid price. Please enter a valid number.")

        item = {
            "item_name": item_name,
            "item_price": item_price
        }

    else:
        print("Invalid option. Please enter 'y' or 'n'.")
        return

    menu[category].append(item)

    with open("menu.json", "w") as file:
        json.dump(menu, file, indent=4)

    print(f"Item '{item_name}' added to {category} successfully!")

def remove_menu_item(menu):
    """Allow the admin to remove an item from the menu."""
    print("\nSelect category from which you want to remove an item:")
    categories = list(menu.keys())
    
    # Displaying the available categories
    count = 1  # Initialize counter
    for category in categories:
        print(f"{count}. {category}")
        count += 1  # Increment counter
    
    try:
        category_choice = int(input("Enter category number: ")) - 1
        if category_choice not in range(len(categories)):
            print("Invalid category selection.")
            return
        category = categories[category_choice]
    except ValueError:
        print("Invalid input. Please enter a number.")
        return

    if not menu[category]:
        print(f"No items available in {category} to remove.")
        return

    print(f"\nItems in {category}:")
    display_menu(menu)  # Show the current items in the selected category

    try:
        item_choice = int(input("Enter item number to remove: ")) - 1
        if item_choice not in range(len(menu[category])):
            print("Invalid item number.")
            return
        item_to_remove = menu[category].pop(item_choice)  # Remove item
    except ValueError:
        print("Invalid input. Please enter a valid number.")
        return

    # Saving the updated menu back to the JSON file
    with open("menu.json", "w") as file:
        json.dump(menu, file, indent=4)

    print(f"Item '{item_to_remove['item_name']}' removed from {category} successfully!")

