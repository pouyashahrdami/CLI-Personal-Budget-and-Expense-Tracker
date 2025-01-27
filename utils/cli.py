from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt
from rich import box
import json
import sys
import os
from datetime import datetime

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from model.user import User
from model.transaction import Transaction

# Initialize console object for rich outputs
console = Console()


def show_welcome():
    console.print("[bold yellow]Welcome to Budget Tracker![/bold yellow]")
    option = Prompt.ask(
        "[bold red]Please log in (1) or register (2):[/bold red]", choices=["1", "2"]
    )

    if option == "1":
        show_login()
    elif option == "2":
        show_register()
    else:
        console.print("[bold red]Invalid choice, please select 1 or 2.[/bold red]")


def show_main_menu():
    # Create a table for the main menu
    table = Table(title="Main Menu", width=100, box=box.ROUNDED)
    table.add_column("Option", justify="center", style="cyan")
    table.add_column("Action", style="magenta")

    # Add rows to the table
    table.add_row("1", "Add Transaction")
    table.add_row("2", "Transaction List")
    table.add_row("3", "View Report")
    table.add_row("4", "Set Budget")
    table.add_row("5", "Predict Future Expenses")
    table.add_row("6", "Change Password")
    table.add_row("7", "Delete Account")
    table.add_row("8", "Exit")

    # Print the table
    console.print(table)

    # Ask user for input
    choice = Prompt.ask(
        "[bold green]Choose an option (1-7):[/bold green]",
        choices=["1", "2", "3", "4", "5", "6", "7", "8"],
    )

    if choice == "1":
        console.clear()
        add_transaction_menu()
    if choice == "2":
        console.clear()
        transaction_list_menu()
    if choice == "7":
        console.clear()
        transaction_list_menu()
    if choice == "8":
        exit_application()


def transaction_list_menu():
    # open the json file
    try:
        with open("data/Transactions.json", "r") as transactionfile:
            transactions = json.load(transactionfile)
            user_transactions = [
                transaction
                for transaction in transactions
                if transaction["username"] == logged_in_user["username"]
            ]

        if user_transactions:
            # show theme in rich table
            table = Table(title="Transaction List", width=100, box=box.ROUNDED)
            table.add_column("NO", justify="center", style="cyan")
            table.add_column("amount", justify="center", style="cyan")
            table.add_column("category", style="magenta")
            table.add_column("date", style="magenta")
            table.add_column("recurring", style="magenta")
            for num, user in enumerate(user_transactions, 1):
                table.add_row(
                    str(num),  # Transaction number
                    str(user["amount"]),  # Amount
                    user["category"],  # Category
                    user["date"],  # Date
                    str(user["recurring"]),  # Recurring
                )
            console.print(table)

        else:
            console.print("no transaction found")

        choice = int(console.input("press 1 to Export as Json : "))
        current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        if choice == 1:
            with open(
                "output/Transactions_"
                + logged_in_user["username"]
                + "_"
                + current_time
                + ".json",
                mode="w+",
            ) as savefile:
                json.dump(user_transactions, savefile, indent=4)
            print("File Saved Sucesfully")
        else:
            print("invalide Choice ")
    except json.JSONDecodeError:
        transactions = []


def add_transaction_menu():
    Username = logged_in_user["username"]
    amount = float(Prompt.ask("[bold blue]Enter Amount for Transaction:[/bold blue]"))
    category = Transaction.select_category()
    date = Prompt.ask("[bold blue]Enter Date for Transaction (YYYY-MM-DD):[/bold blue]")
    recurring = (
        Prompt.ask("[bold blue]Is this a recurring transaction? (yes/no):[/bold blue]")
        .strip()
        .lower()
        == "yes"
    )

    transaction = Transaction(amount, category, date, recurring)
    transaction.add_transcation(Username, amount, category, date, recurring)


def show_register():
    username = Prompt.ask("[bold red]Please Enter Your Username:[/bold red]")
    password = Prompt.ask(
        "[bold red]Please Enter Your Password (min 4 characters):[/bold red]"
    )

    if username and password:
        registration(username, password)
    else:
        console.print("[bold red]Username and password are required![/bold red]")


def show_login():
    username = Prompt.ask("[bold red]Please Enter Your Username:[/bold red]")
    password = Prompt.ask("[bold red]Please Enter Your Password:[/bold red]")

    if username and password:
        verification(username, password)
    else:
        console.print("[bold red]Username and password are required![/bold red]")


def verification(username, password):
    global logged_in_user
    try:
        with open("data/users.json", mode="r", encoding="utf-8") as userdata:
            user_details = json.load(userdata)
    except Exception as e:
        console.print(f"[bold red]Error reading user data: {e}[/bold red]")
        return False

    user = check_username(username, user_details)
    if user is None:
        console.print("[bold red]User does not exist.[/bold red]")
        return False

    stored_hash = user["password"].encode("utf-8")
    user_instance = User(username, stored_hash)

    if user_instance.check_password(password):
        console.print("[bold green]Login successful![/bold green]")
        logged_in_user = user
        show_main_menu()
        return True
    else:
        console.print("[bold red]Incorrect password.[/bold red]")
        return False


def registration(username, password):
    # Remove any spaces in the username
    username = username.replace(" ", "")
    user_details = []

    try:
        with open("data/users.json", mode="r", encoding="utf-8") as userdata:
            user_details = json.load(userdata)
    except json.JSONDecodeError:
        user_details = []

    # Check if the username already exists
    for user in user_details:
        if user["username"] == username:
            console.print(
                "[bold red]Username already exists! Please choose a different one.[/bold red]"
            )
            return False

    # Ensure password length is at least 4 characters
    if len(password) < 4:
        console.print(
            "[bold red]Password must be at least 4 characters long![/bold red]"
        )
        return False

    # Create the new user and save it
    user = User(username, password)
    user_json = {"username": username, "password": user.password.decode("utf-8")}
    user_details.append(user_json)

    with open("data/users.json", mode="w", encoding="utf-8") as task_file:
        json.dump(user_details, task_file, indent=4)

    console.print("[bold green]Registration Complete![/bold green]")

    return True


def check_username(username, user_details):
    for user in user_details:
        if user["username"] == username:
            return user
    return None


def check_password(password):
    return User.check_password(password)


def exit_application():
    exit()
