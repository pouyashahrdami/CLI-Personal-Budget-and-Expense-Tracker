from rich.console import Console
from rich.table import Table
import json
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from model.user import User

console = Console()


def show_welcome():
    console.print("[bold yellow ]welcome to budget tracker[/bold yellow ]")
    option = int(
        console.input("[bold red ]please log in (1) or register (2) [/bold red ] : ")
    )
    if option == 1:
        show_login()
    elif option == 2:
        show_register()
    else:
        console.print("wrong choice")


def show_register():
    username = console.input("[bold red ]Please Enter Your Username[/bold red ] : ")
    password = console.input("[bold red ]Please Enter Your password[/bold red ] : ")
    if username and password:
        registration(username, password)
        if registration:
            console.clear()
            show_welcome()
    else:
        console.print("you must enter username and password")


def show_login():
    username = console.input("[bold red ]Please Enter Your Username[/bold red ] : ")
    password = console.input("[bold red ]Please Enter Your password[/bold red ] : ")
    if username and password:
        verfication(username, password)
    else:
        console.print("you must enter username and password")


def show_main_menu():
    table = Table(title="Main Menu", width=100)
    table.add_column("option", justify="center", style="cyan")
    table.add_column("Action")
    table.add_row("1", "Add Transaction")
    table.add_row("2", "View Report")
    table.add_row("3", "Set Budget")
    table.add_row("4", "Predict Future expenses")
    table.add_row("5", "Change Password")
    table.add_row("6", "Delete Account")
    table.add_row("7", "Exit")
    console.print(table)




def verfication(username, password):
    try:
        with open("data/users.json", mode="r", encoding="utf-8") as userdata:
            user_details = json.load(userdata)
    except Exception as e:
        console.print(f"Error reading user data: {e}")
        return False

    user = check_username(username, user_details)
    if user is None:
        console.print("User does not exist.")
        return False

    stored_hash = user["password"].encode('utf-8')
    user_instance = User(username, stored_hash)
    
    if user_instance.check_password(password):
        console.print("Login successful!")
        show_main_menu()
        return True
    else:
        console.print("Incorrect password.")
        return False

def registration(username, password):
    # no space in username
    username = username.replace(" ", "")
    user_details = []
    # if the username exists
    try:
        with open("data/users.json", mode="r", encoding="utf-8") as userdata:
            user_details = json.load(userdata)
    except json.JSONDecodeError:
        user_details = []

    for user in user_details:
        if user["username"] == username:
            print("user name exists")
            return False
            
    # password len must be 4 digits
    if len(password) <= 4:
        print("password len must be at greater 4")
        return False
    
    user = User(username , password)
    # -----------------------------------------------------------
    user_json = {
        "username": username,
        "password": user.password.decode('utf-8')
    }
    user_details.append(user_json)
    with open("data/users.json", mode="w", encoding="utf-8") as task_file:
        json.dump(user_details, task_file, indent=4)
    console.print("registration Complete")
    
    return True



def check_username(username, user_details):
    for user in user_details:
        if user["username"] == username:
            return user
    return None


def check_password(password):
    return User.check_password(password)


def user_choice():
    return int(console.input("choose and option (1 - 7)"))



