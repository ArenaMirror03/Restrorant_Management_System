import json
import datetime
import uuid
from Authentication.Menu.menu import display_menu

# This variable will keep track of the last order number to generate the next one
last_order_number = 0

def place_order(menu):
    """Allow customers to place an order."""
    global last_order_number  # Access the global last_order_number
    
    orders = []
    
    display_menu(menu)
    
    order_id = generate_order_id()  # Generate a unique order ID
    order_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Get current date and time
    
    while True:
        order_input = input("Enter the items you want to order (Dal, Roti, Ice Cream): ")
        items = [item.strip().lower() for item in order_input.split(",")]

        for category in ["Breakfast", "Lunch", "Dinner", "Beverages"]:
            for item in menu[category]:
                if item['item_name'].lower() in items:
                    if 'half_plate_price' in item or 'full_plate_price' in item:
                        plate_choice = input(f"How many plates of {item['item_name']} would you like to order? (half/full): ").strip().lower()
                        if plate_choice == 'half' and 'half_plate_price' in item:
                            quantity = int(input(f"How many half plates of {item['item_name']} would you like to order? "))
                            orders.append({"item_name": item['item_name'], "price": item['half_plate_price'], "quantity": quantity, "order_id": order_id, "order_time": order_time})
                        elif plate_choice == 'full' and 'full_plate_price' in item:
                            quantity = int(input(f"How many full plates of {item['item_name']} would you like to order? "))
                            orders.append({"item_name": item['item_name'], "price": item['full_plate_price'], "quantity": quantity, "order_id": order_id, "order_time": order_time})
                        else:
                            print(f"Invalid plate option for {item['item_name']}. Skipping.")
                    else:
                        orders.append({"item_name": item['item_name'], "price": item['item_price'], "quantity": 1, "order_id": order_id, "order_time": order_time})
                    
        another_order = input("Would you like to add another item to your order? (y/n): ").strip().lower()
        if another_order != 'y':
            break

    save_order_to_file(orders)  # Save orders to a JSON file
    return orders

def generate_order_id():
    """Generate a new order ID in the format ORD001, ORD002, etc."""
    global last_order_number  # Access the global last_order_number
    last_order_number += 1  # Increment the last order number
    order_id = f"ORD{last_order_number:03d}"  # Format the order number with leading zeros
    return order_id

def save_order_to_file(orders):
    """Save the order details to a JSON file with proper indentation."""
    date_today = datetime.datetime.now().strftime("%Y-%m-%d")
    filename = f"{date_today}_orders.json"
    
    try:
        # Write the orders to the JSON file with indentation
        with open(filename, "w") as file:  # Use "w" to overwrite the file
            json.dump(orders, file, indent=4)  # Save the entire list of orders with indentation
        print(f"Order details saved to {filename}.")
        print(f"Your Order ID is: {orders[0]['order_id']}")  # Display the order ID after saving
    except Exception as e:
        print(f"Error saving order details: {e}")

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
        print(f"{order['item_name']} x{order['quantity']} - {order['price'] * order['quantity']:.2f} (Order ID: {order['order_id']}, Time: {order['order_time']})")
    print(f"\nTotal: {total:.2f}")
    print(f"GST (18%): {gst:.2f}")
    print(f"Total Amount: {total_amount:.2f}")

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
                                orders.append({"item_name": item['item_name'], "price": item['half_plate_price'], "quantity": quantity, "order_id": orders[0]['order_id'], "order_time": orders[0]['order_time']})  # Use the same order ID and time
                            elif plate_choice == 'full' and 'full_plate_price' in item:
                                quantity = int(input(f"How many full plates of {item['item_name']} would you like to order? "))
                                orders.append({"item_name": item['item_name'], "price": item['full_plate_price'], "quantity": quantity, "order_id": orders[0]['order_id'], "order_time": orders[0]['order_time']})  # Use the same order ID and time
                            else:
                                print(f"Invalid plate option for {item['item_name']}. Skipping.")
                        else:
                            orders.append({"item_name": item['item_name'], "price": item['item_price'], "quantity": 1, "order_id": orders[0]['order_id'], "order_time": orders[0]['order_time']})  # Use the same order ID and time

        elif modify_choice == "2":
            # Remove item from order
            print("\nYour current orders:")
            count = 1  # Initialize a counter
            for order in orders:
                print(f"{count}. {order['item_name']} x{order['quantity']} (Order ID: {order['order_id']}, Time: {order['order_time']})")
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
            break  # Exit modification loop
        else:
            print("Invalid option. Please enter '1', '2', or '3'.")

def cancel_order(orders):
    """Allow the customer to cancel an ongoing order by order ID."""
    if not orders:
        print("You have not placed any orders yet.")
        return orders

    while True:
        order_id = input("Enter the Order ID to cancel (or type 'back' to go back): ").strip()
        
        if order_id.lower() == 'back':
            break

        order_found = False
        for order in orders:
            if order['order_id'] == order_id:
                orders.remove(order)
                print(f"Order ID {order_id} has been canceled successfully.")
                order_found = True
                break

        if order_found:
            save_order_to_file(orders)
            break
        else:
            print("Order ID not found. Please try again.")
