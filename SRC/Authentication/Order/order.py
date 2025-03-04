import datetime
from Authentication.Menu.menu import display_menu

def place_order(menu):
    """Allow customers to place an order."""
    orders = []
    
    display_menu(menu)
    
    while True:
        order_input = input("Enter the items you want to order ( Dal, Roti, Ice Cream): ")
        items = [item.strip().lower() for item in order_input.split(",")]

        for category in ["Breakfast", "Lunch", "Dinner", "Beverages"]:
            for item in menu[category]:
                if item['item_name'].lower() in items:
                    if 'half_plate_price' in item or 'full_plate_price' in item:
                        plate_choice = input(f"How many plates of {item['item_name']} would you like to order? (half/full): ").strip().lower()
                        if plate_choice == 'half' and 'half_plate_price' in item:
                            quantity = int(input(f"How many half plates of {item['item_name']} would you like to order? "))
                            orders.append({"item_name": item['item_name'], "price": item['half_plate_price'], "quantity": quantity})
                        elif plate_choice == 'full' and 'full_plate_price' in item:
                            quantity = int(input(f"How many full plates of {item['item_name']} would you like to order? "))
                            orders.append({"item_name": item['item_name'], "price": item['full_plate_price'], "quantity": quantity})
                        else:
                            print(f"Invalid plate option for {item['item_name']}. Skipping.")
                    else:
                        orders.append({"item_name": item['item_name'], "price": item['item_price'], "quantity": 1})
                    
        another_order = input("Would you like to add another item to your order? (y/n): ").strip().lower()
        if another_order != 'y':
            break

    return orders


def generate_bill(orders):
    """Generate a bill for the customer."""
    if len(orders) == 0:
        print("No items ordered.")
        return

    total = 0
    for order in orders:
        total += order['price'] * order['quantity']

    gst = total * 0.18  # 18% GST
    total_amount = total + gst

    print("\n--- Bill ---")
    for order in orders:
        print(f"{order['item_name']} x{order['quantity']} - {order['price'] * order['quantity']:.2f}")
    print(f"\nTotal: {total:.2f}")
    print(f"GST (18%): {gst:.2f}")
    print(f"Total Amount: {total_amount:.2f}")

    date_today = datetime.datetime.now().strftime("%Y-%m-%d")
    with open(f"{date_today}_billing.txt", "a") as file:
        for order in orders:
            file.write(f"{order['item_name']} x{order['quantity']} - {order['price'] * order['quantity']:.2f}\n")
        file.write(f"Total: {total:.2f}\n")
        file.write(f"GST: {gst:.2f}\n")
        file.write(f"Total Amount: {total_amount:.2f}\n\n")


def modify_order(orders, menu):
    """Allow the customer to add or remove items from their ongoing order."""
    if not orders:  # Check if there are no orders
        print("You have not placed any orders yet. Please place an order first.")
        return orders  # Return the unchanged orders list

    while True:
        print("\n--- Modify Ongoing Order ---")
        print("1. Add item to order")
        print("2. Remove item from order")
        print("3. Cancel modification")
        
        modify_choice = input("Enter your choice: ")

        if modify_choice == "1":
            # Add item to order
            order_input = input("Enter the items you want to add to your order: ")
            items = [item.strip().lower() for item in order_input.split(",")]

            for category in ["Breakfast", "Lunch", "Dinner", "Beverages"]:
                for item in menu[category]:
                    if item['item_name'].lower() in items:
                        if 'half_plate_price' in item or 'full_plate_price' in item:
                            plate_choice = input(f"How many plates of {item['item_name']} would you like to order? (half/full): ").strip().lower()
                            if plate_choice == 'half' and 'half_plate_price' in item:
                                quantity = int(input(f"How many half plates of {item['item_name']} would you like to order? "))
                                orders.append({"item_name": item['item_name'], "price": item['half_plate_price'], "quantity": quantity})
                            elif plate_choice == 'full' and 'full_plate_price' in item:
                                quantity = int(input(f"How many full plates of {item['item_name']} would you like to order? "))
                                orders.append({"item_name": item['item_name'], "price": item['full_plate_price'], "quantity": quantity})
                            else:
                                print(f"Invalid plate option for {item['item_name']}. Skipping.")
                        else:
                            orders.append({"item_name": item['item_name'], "price": item['item_price'], "quantity": 1})

        elif modify_choice == "2":
            # Remove item from order
            print("\nYour current orders:")
            count = 1  # Initialize a counter
            for order in orders:
                print(f"{count}. {order['item_name']} x{order['quantity']}")
                count += 1  # Increment the counter

            try:
                remove_item_index = int(input("Enter the item number to remove from your order: ")) - 1
                if 0 <= remove_item_index < len(orders):
                    removed_order = orders.pop(remove_item_index)
                    print(f"Removed {removed_order['item_name']} from your order.")
                else:
                    print("Invalid item number.")
            except ValueError:
                print("Invalid input. Please enter a valid number.")

        elif modify_choice == "3":
            # Cancel modification
            break
        else:
            print("Invalid option. Please enter '1', '2', or '3'.")

    return orders