from Authentication.Menu.menu import load_menu, display_menu, add_menu_item
from Authentication.Order.order import place_order, generate_bill, modify_order

def main():
    menu = load_menu()  # Load the menu for customer view
    orders = []  # Initialize the orders list

    while True:
        print("\n--- Restaurant Management System ---")
        print("1. Customer")
        choice = input("Enter choice (1/2): ")

        if choice == "1":
            while True:
                print("\nCustomer Options:")
                print("1. Display Menu")
                print("2. Place Order")
                print("3. Modify Ongoing Order")
                print("4. View Ongoing Orders")
                print("5. Generate Bill")
                print("6. Add Menu Item")
                print("7. Exit")
                customer_choice = input("Enter choice: ")

                if customer_choice == "1":
                    display_menu(menu)  # Display the menu in a table format
                elif customer_choice == "2":
                    orders = place_order(menu)  # Place the order
                elif customer_choice == "3":
                    orders = modify_order(orders, menu)  # Modify ongoing order
                elif customer_choice == "4":
                    if orders:
                        print("\n--- Ongoing Orders ---")
                        for order in orders:
                            print(f"{order['item_name']} x{order['quantity']}")
                    else:
                        print("No ongoing orders.")
                elif customer_choice == "5":
                    generate_bill(orders)  # Generate bills 
                elif customer_choice == "6":
                    add_menu_item()  # Add new menu item
                    menu = load_menu()  # Reload the updated menu after addition
                elif customer_choice == "7":
                    break


main()
