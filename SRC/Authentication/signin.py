import json
import maskpass
import os
import logging


database_folder = r"C:\Users\dell\Desktop\final\Restrorant_Management_System\SRC\Authentication\Database"
path = os.getcwd()
LOG_FOLDER = os.path.join(path,'SRC','Logs','Application_log.txt')


if not os.path.exists(database_folder):
    os.makedirs(database_folder)
if not os.path.exists(LOG_FOLDER):
    os.makedirs(LOG_FOLDER)


log_file = os.path.join(LOG_FOLDER, 'signin.log')
logging.basicConfig(
    filename=log_file,
    level=logging.ERROR,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

def sign_in(admin_id, password):
    """Admin sign-in function to validate credentials."""
    try:
        with open(os.path.join(database_folder, "admin_data.json"), "r") as file:
            data = json.load(file)
    except FileNotFoundError:
        logging.error(f"File {os.path.join(database_folder, 'admin_data.json')} not found.")
        print("\033[91mNo admin data found. Please sign up first.\033[0m")
        return False

    if admin_id in data and data[admin_id]["password"] == password:
        print("\033[92mAdmin signed in successfully!\033[0m")
        return True
    else:
        logging.warning(f"Failed sign-in attempt for admin ID: {admin_id}. Invalid credentials.")
        print("\033[91mInvalid credentials!\033[0m")
        return False

if __name__ == "__main__":
    try:
        admin_id = input("Enter Admin ID: ")
        password = maskpass.askpass('Password: ', mask='*')  
        sign_in(admin_id, password)
    except Exception as e:
        logging.error(f"Unexpected error during sign-in: {e}")
        print("\033[91mAn error occurred during sign-in. Please check the log file.\033[0m")
