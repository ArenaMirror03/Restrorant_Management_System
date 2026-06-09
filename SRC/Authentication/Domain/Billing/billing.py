import datetime
import os
import logging


database_folder = r"C:\Users\dell\Desktop\final\Restrorant_Management_System\SRC\Authentication\Database"


if not os.path.exists(database_folder):
    os.makedirs(database_folder)


path = os.getcwd()
LOG_FOLDER = os.path.join(path,'SRC','Logs','Application_log.txt')

if not os.path.exists(LOG_FOLDER):
    os.makedirs(LOG_FOLDER)

log_file = os.path.join(LOG_FOLDER, 'billing.log')
logging.basicConfig(
    filename=log_file,
    level=logging.DEBUG,  
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

def generate_bill(orders):
    """Generate a bill for the customer and store it in a file."""
    
    if not orders:
        logging.warning("No items ordered. Cannot generate bill.")
        print("No items ordered.")
        return

    try:
       
        total = sum(order['price'] * order['quantity'] for order in orders)
        gst = total * 0.18  # 18% GST
        total_amount = total + gst

        
        current_date = datetime.datetime.now().strftime("%Y-%m-%d")
        current_time = datetime.datetime.now().strftime("%H:%M:%S")

        
        bill_file = os.path.join(database_folder, f"{current_date}_bill.txt")

        
        with open(bill_file, 'a') as file:
            file.write("\n--- Bill ---\n")
            for order in orders:
                file.write(f"{order['item_name']} x{order['quantity']} - {order['price'] * order['quantity']:.2f}\n")

            file.write(f"\nTotal: {total:.2f}\n")
            file.write(f"GST (18%): {gst:.2f}\n")
            file.write(f"Total Amount: {total_amount:.2f}\n")
            file.write(f"Time of Billing: {current_time}\n")
            file.write(f"\n--- End of Bill ---\n")

    
        print("\n--- Bill ---")
        for order in orders:
            print(f"{order['item_name']} x{order['quantity']} - {order['price'] * order['quantity']:.2f}")

        print(f"\nTotal: {total:.2f}")
        print(f"GST (18%): {gst:.2f}")
        print(f"Total Amount: {total_amount:.2f}")
        print(f"Time of Billing: {current_time}")
        print(f"\nBill has been saved to {bill_file}")
        
        logging.info(f"Bill generated and saved to {bill_file}. Total: {total:.2f}, GST: {gst:.2f}, Total Amount: {total_amount:.2f}")

    except Exception as e:
        logging.error(f"Error during bill generation: {e}")
        print("\033[91mAn error occurred during bill generation. Please check the log file.\033[0m")
