import json
import uuid

def sign_up(password, name, age, worktype):
    """Admin sign-up function where Admin ID is auto-generated."""
    admin_id = "VS" + str(uuid.uuid4().int)[:5]  # Generate ID like 'VS101'

    admin_data = {
        "admin_id": admin_id,
        "password": password,
        "name": name,
        "age": age,
        "worktype": worktype
    }

    try:
        with open("admin_data.json", "r") as file:
            data = json.load(file)
    except FileNotFoundError:
        data = {}

    if admin_id in data:
        print(f"Admin ID '{admin_id}' already exists. Please try again.")
        return

    data[admin_id] = admin_data

    with open("admin_data.json", "w") as file:
        json.dump(data, file, indent=4)

    print(f"Admin signed up successfully! Your Admin ID is {admin_id}")


def sign_in(admin_id, password):
    """Admin sign-in function to validate credentials."""
    try:
        with open("admin_data.json", "r") as file:
            data = json.load(file)
    except FileNotFoundError:
        data = {}

    if admin_id in data and data[admin_id]["password"] == password:
        print("Admin signed in successfully!")
        return True
    else:
        print("Invalid credentials!")
        return False