from Authentication.Menu.menu import load_menu, display_menu, remove_menu_item, add_menu_item
from Authentication.Order.order import place_order, generate_bill, modify_order, cancel_order
from Authentication.admin import sign_up, sign_in
from Authentication.Table_Booking.Table import cancel_booking, release_table, display_tables, book_tables

def main():
    while True:
        # Main menu for choosing Admin or Customer
        print("\nWelcome to the Restaurant Management System")
        print("1. Admin")
        print("2. Customer")
        print("3. Exit")
        choice = input("Please enter your choice (1/2/3): ")

        if choice == '1':  # Admin section
            print("\n--- Admin Panel ---")
            print("1. Sign Up")
            print("2. Sign In")
            admin_choice = input("Please select an option (1/2): ")

            if admin_choice == '1':  # Admin sign-up
                name = input("Enter your name: ")
                age = input("Enter your age: ")
                worktype = input("Enter your worktype: ")
                password = input("Enter your password: ")

                sign_up(password, name, age, worktype)

            elif admin_choice == '2':  # Admin sign-in
                admin_id = input("Enter your Admin ID: ")
                password = input("Enter your password: ")

                if sign_in(admin_id, password):
                    print("\n--- Admin Dashboard ---")
                    menu = load_menu()

                    while True:
                        print("\n1. Display Menu")
                        print("2. Add Menu Item")
                        print("3. Remove Menu Item")
                        print("4. Cancel Order")
                        print("5. Cancel Table")
                        print("6. Logout")
                        admin_action = input("Select action: ")

                        if admin_action == '1':
                            display_menu(menu)
                        elif admin_action == '2':
                            add_menu_item()
                        elif admin_action == '3':
                            remove_menu_item(menu)
                        elif admin_action == '4':
                            cancel_order(menu)
                        elif admin_action == '5':
                            cancel_booking()  # Function to cancel a table booking
                        elif admin_action == '6':
                            print("Logged out successfully.")
                            break
                        else:
                            print("Invalid choice. Please try again.")

                else:
                    print("Failed to sign in. Please check your credentials.")

        elif choice == '2':  # Customer section
            print("\n--- Customer Panel ---")
            menu = load_menu()
            orders = []  # Initialize empty orders list

            while True:
                print("\n1. Dispaly Menu")
                print("2. Place Order")
                print("3. Display Tables")
                print("4. Book Table")
                print("5. Modify Order")
                print("6. Generate Bill")
                print("7. Release Table")
                print("8. Exit")
                customer_choice = input("Please select an option (1/2/3/4/5/6/7): ")

                if customer_choice == '1':  # Place order
                    display_menu(menu)
                if customer_choice == '2':  # Place order
                    orders = place_order(menu)
                elif customer_choice == '3':  # Display tables
                    display_tables()
                elif customer_choice == '4':  # Book table
                    book_tables()
                elif customer_choice == '5':  # Modify order
                    orders = modify_order(orders, menu)
                elif customer_choice == '6':  # Generate bill
                    generate_bill(orders)
                elif customer_choice == '7':  # Release table
                    release_table()
                elif customer_choice == '8':  # Exit customer panel
                    print("Thank you for visiting. Goodbye!")
                    break
                else:
                    print("Invalid choice. Please try again.")

        elif choice == '3':  # Exit program
            print("Exiting the system. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()