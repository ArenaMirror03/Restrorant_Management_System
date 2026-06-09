import json
import uuid
import os
import logging


database_folder = r"C:\Users\dell\Desktop\final\Restrorant_Management_System\SRC\Authentication\Database"
path = os.getcwd()
LOG_FOLDER = os.path.join(path,'SRC','Logs','Application_log.txt')


if not os.path.exists(database_folder):
    os.makedirs(database_folder)
if not os.path.exists(LOG_FOLDER):
    os.makedirs(LOG_FOLDER)

log_file = os.path.join(LOG_FOLDER, 'signup.log')
logging.basicConfig(
    filename=log_file,
    level=logging.ERROR,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

def sign_up(password, name, age, worktype):
    """Admin sign-up function where Admin ID is auto-generated."""
    admin_id = "VS" + str(uuid.uuid4().int)[:3]  

    admin_data = {
        "admin_id": admin_id,
        "password": password,
        "name": name,
        "age": age,
        "worktype": worktype
    }

    admin_data_file = os.path.join(database_folder, "admin_data.json")

    try:
      
        with open(admin_data_file, "r") as file:
            data = json.load(file)
    except FileNotFoundError:
        data = {}
        logging.error(f"File {admin_data_file} not found. A new file will be created.")

    data[admin_id] = admin_data 

    try:
      
        with open(admin_data_file, "w") as file:
            json.dump(data, file, indent=4)
        print(f"\033[92mAdmin signed up successfully! Your Admin ID is {admin_id}\033[0m")
    except Exception as e:
       
        logging.error(f"Error saving data to {admin_data_file}: {e}")
        print("\033[91mError saving admin data. Please try again.\033[0m")

if __name__ == "__main__":
   
    try:
        password = input("Enter Password: ")
        name = input("Enter Name: ")
        age = input("Enter Age: ")
        worktype = input("Enter Work Type: ")
        
        sign_up(password, name, age, worktype)
    except Exception as e:
        logging.error(f"Unexpected error during sign-up: {e}")
        print("\033[91mAn error occurred during sign-up. Please check the log file.\033[0m")
