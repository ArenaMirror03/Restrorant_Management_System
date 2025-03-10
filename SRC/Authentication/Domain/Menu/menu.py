import json
import os
import logging
from tabulate import tabulate

database_folder = r"C:\Users\dell\Desktop\final\Restrorant_Management_System\SRC\Authentication\Database"


if not os.path.exists(database_folder):
    os.makedirs(database_folder)


path = os.getcwd()
LOG_FOLDER = os.path.join(path,'SRC','Logs','Application_log.txt') # Path to log folder

if not os.path.exists(LOG_FOLDER):
    os.makedirs(LOG_FOLDER)

log_file = os.path.join(LOG_FOLDER, 'menu.log')
logging.basicConfig(
    filename=log_file,
    level=logging.DEBUG,  
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

def load_menu():
    """Load the menu data from a JSON file stored in the Database folder."""
    menu_file = os.path.join(database_folder, "menu.json")
    
    try:
        with open(menu_file, "r") as file:
            menu = json.load(file)
            logging.info("Menu loaded successfully.")
    except FileNotFoundError:
       
        menu = {
            "Breakfast": [],
            "Lunch": [],
            "Dinner": [],
            "Beverages": []
        }
        logging.warning("Menu file not found. Initializing empty menu.")
    
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
            count = 1 
            for item in menu[category]:
                if 'item_price' in item:
                    row = [count, item['item_name'], f"{item['item_price']}", "N/A", "N/A"]
                elif 'half_plate_price' in item and 'full_plate_price' in item:
                    row = [count, item['item_name'], "N/A", f"{item['half_plate_price']}", f"{item['full_plate_price']}"]
                else:
                    row = [count, item['item_name'], "N/A", "N/A", "N/A"]
                
                table.append(row)
                count += 1 

            headers = ["Item No.", "Item Name", "Single Item", "Half Plate", "Full Plate"]
            purple = '\033[35m'
            reset = '\033[0m'
            
            print(f"{purple}{tabulate(table, headers, tablefmt='grid')}{reset}")

def add_menu_item():
    """Allow the admin to add an item to the menu."""
    menu = load_menu()

    print("\nSelect category to add item:")
    categories = list(menu.keys())
    
    count = 1 
    for category in categories:
        print(f"{count}. {category}")
        count += 1  

    try:
        category_choice = int(input("Enter category number: ")) - 1
        if category_choice not in range(len(categories)):
            print("Invalid category selection.")
            return
        category = categories[category_choice]
    except ValueError:
        print("Invalid input. Please enter a number.")
        logging.error("Invalid category input.")
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
        logging.warning("Invalid input for quantity options. Expected 'y' or 'n'.")
        return

    menu[category].append(item)

   
    menu_file = os.path.join(database_folder, "menu.json")
    try:
        with open(menu_file, "w") as file:
            json.dump(menu, file, indent=4)
        logging.info(f"Item '{item_name}' added to {category} successfully.")
    except Exception as e:
        logging.error(f"Error saving menu: {e}")
        print("\033[91mError saving the menu. Please check the log file.\033[0m")
        
        green = '\033[32m'
        reset = '\033[0m'

    print(f"{green}Item '{item_name}' added to {category} successfully!{reset}")

def remove_menu_item(menu):
    """Allow the admin to remove an item from the menu."""
    print("\nSelect category from which you want to remove an item:")
    categories = list(menu.keys())
    
    
    count = 1 
    for category in categories:
        print(f"{count}. {category}")
        count += 1 
    try:
        category_choice = int(input("Enter category number: ")) - 1
        if category_choice not in range(len(categories)):
            print("Invalid category selection.")
            return
        category = categories[category_choice]
    except ValueError:
        print("Invalid input. Please enter a number.")
        logging.error("Invalid category input.")
        return

    if not menu[category]:
        print(f"No items available in {category} to remove.")
        logging.warning(f"No items in category '{category}' to remove.")
        return

    print(f"\nItems in {category}:")
    display_menu(menu)  

    try:
        item_choice = int(input("Enter item number to remove: ")) - 1
        if item_choice not in range(len(menu[category])):
            print("Invalid item number.")
            return
        item_to_remove = menu[category].pop(item_choice)  
    except ValueError:
        print("Invalid input. Please enter a valid number.")
        logging.error("Invalid item number input.")
        return

    
    menu_file = os.path.join(database_folder, "menu.json")
    try:
        with open(menu_file, "w") as file:
            json.dump(menu, file, indent=4)
        logging.info(f"Item '{item_to_remove['item_name']}' removed from {category} successfully.")
    except Exception as e:
        logging.error(f"Error saving menu: {e}")
        print("\033[91mError saving the menu. Please check the log file.\033[0m")
        red = '\033[31m'
        reset = '\033[0m'

    print(f"{red}Item '{item_to_remove['item_name']}' removed from {category} successfully!{reset}")
