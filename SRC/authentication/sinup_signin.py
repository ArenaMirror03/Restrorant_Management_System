import json
import os
import re

def load_admin_data():
    """Load admin data from JSON file, creating the file if it doesn't exist."""
    if not os.path.exists("admin_data.json"):
        with open("admin_data.json", "w") as file:
            json.dump({}, file) 
    with open("admin_data.json", "r") as file:
        return json.load(file) or {} 

def save_admin_data(data):
    """Save admin data to JSON file."""
    with open("admin_data.json", "w") as file:
        json.dump(data, file, indent=4)

def sign_up():
    while True:
        try:
            admin_id = int(input("Enter Admin ID: "))
            if admin_id >= 1:
                break
            else:
                print("Invalid input! Please enter a digit greater than or equal to 1.")
        except ValueError:
            print("Invalid input! Please enter a valid digit.")   

    while True:
        password = input('Enter Password: ')
        if len(password) >= 8 and re.match(r'^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$#])[A-Za-z\d@$#]+$', password):
            break
        else:
            print("Password should be at least 8 characters long and a combination of letters [A-Z], digits [0-9], and punctuation marks [@$#].")

    while True:
        name = input("Enter your name: ")
        if name.isalpha() and (2 < len(name) <= 20):
            break
        else:
            print("Invalid input! Please enter a valid name.")

    while True:
        try:
            age = int(input("Enter your age: "))
            if 0 <= age <= 100:
                break
            else:
                print("Invalid input! Please enter an age between 0 and 100.")
        except ValueError:
            print("Invalid input! Please enter a valid digit.")   

    while True:
        worktype = input("Enter your work type: ")
        if worktype.isalpha() and (2 < len(worktype) <= 20):
            break
        else:
            print("Invalid input! Please enter a valid work type.")

    admin_data = {
        "admin_id": admin_id,
        "password": password,
        "name": name,
        "age": age,
        "worktype": worktype
    }

    data = load_admin_data()

    if str(admin_id) in data:
        print(f"Admin ID '{admin_id}' already exists. Please try again.")
        return  # Exit the sign_up function to allow retry

    data[str(admin_id)] = admin_data
    save_admin_data(data)

    print(f"Admin signed up successfully! Your Admin ID is {admin_id}")

def sign_in():
    admin_id = input("Enter Admin ID: ")
    password = input("Enter password: ")

    data = load_admin_data()

    if str(admin_id) in data and data[str(admin_id)]["password"] == password:
        print("Admin signed in successfully!")
        return True
    else:
        print("Invalid credentials!")
        return False

while True:
    print(">>>> Press 1 for SignUp ")
    print(">>>> Press 2 for Signin ")
    print(">>>> Press 3 for Exit ")

    try:
        choice = int(input("Enter your choice: ")) 
    except ValueError:
        print("Invalid input! Please enter a digit (1, 2, or 3).")
        continue

    if choice == 1:
        sign_up()
    elif choice == 2:
        sign_in()   
    elif choice == 3:
        print("Exiting the program. Goodbye!")
        break
    else:
        print("Invalid choice! Please enter (1, 2, or 3).")
        import json
import os
import re

def load_admin_data():
    """Load admin data from JSON file, creating the file if it doesn't exist."""
    if not os.path.exists("admin_data.json"):
        with open("admin_data.json", "w") as file:
            json.dump({}, file) 
    with open("admin_data.json", "r") as file:
        return json.load(file) or {} 

def save_admin_data(data):
    """Save admin data to JSON file."""
    with open("admin_data.json", "w") as file:
        json.dump(data, file, indent=4)

def sign_up():
    while True:
        try:
            admin_id = int(input("Enter Admin ID: "))
            if admin_id >= 1:
                break
            else:
                print("Invalid input! Please enter a digit greater than or equal to 1.")
        except ValueError:
            print("Invalid input! Please enter a valid digit.")   

    while True:
        password = input('Enter Password: ')
        if len(password) >= 8 and re.match(r'^(?=.[A-Za-z])(?=.\d)(?=.*[@$#])[A-Za-z\d@$#]+$', password):
            break
        else:
            print("Password should be at least 8 characters long and a combination of letters [A-Z], digits [0-9], and punctuation marks [@$#].")

    while True:
        name = input("Enter your name: ")
        if name.isalpha() and (2 < len(name) <= 20):
            break
        else:
            print("Invalid input! Please enter a valid name (only letters, 3-20 characters).")

    while True:
        try:
            age = int(input("Enter your age: "))
            if 0 <= age <= 100:
                break
            else:
                print("Invalid input! Please enter an age between 0 and 100.")
        except ValueError:
            print("Invalid input! Please enter a valid digit.")   

    while True:
        worktype = input("Enter your work type: ")
        if re.match(r'^[A-Za-z ]+$', worktype) and (2 < len(worktype) <= 20):
            break
        else:
            print("Invalid input! Please enter a valid work type (letters and spaces only, 3-20 characters).")

    admin_data = {
        "admin_id": str(admin_id),  # Store admin_id as a string to avoid type mismatch
        "password": password,
        "name": name,
        "age": age,
        "worktype": worktype
    }

    data = load_admin_data()

    if str(admin_id) in data:
        print(f"Admin ID '{admin_id}' already exists. Please try again.")
        return  # Exit the sign_up function to allow retry

    data[str(admin_id)] = admin_data
    save_admin_data(data)

    print(f"Admin signed up successfully! Your Admin ID is {admin_id}")

def sign_in():
    admin_id = input("Enter Admin ID: ")  # Keep input as string to match stored data
    password = input("Enter password: ")

    data = load_admin_data()

    if admin_id in data and data[admin_id]["password"] == password:
        print("Admin signed in successfully!")
        return True
    else:
        print("Invalid credentials!")
        return False

while True:
    print(">>>> Press 1 for SignUp ")
    print(">>>> Press 2 for Signin ")
    print(">>>> Press 3 for Exit ")

    try:
        choice = int(input("Enter your choice: ")) 
    except ValueError:
        print("Invalid input! Please enter a digit (1, 2, or 3).")
        continue

    if choice == 1:
        sign_up()
    elif choice == 2:
        sign_in()   
    elif choice == 3:
        print("Exiting the program. Goodbye!")
        break
    else:
        print("Invalid choice! Please enter (1, 2, or 3).")