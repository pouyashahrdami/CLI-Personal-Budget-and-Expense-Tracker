from datetime import datetime
import json

class Transaction:
    categories = ["food", "Bills", "Health"]

    def __init__(self, amount, category, date, recurring):
        self.amount = amount
        self.category = category
        self.date = datetime.strptime(date, "%Y-%m-%d")
        self.recurring = recurring

    def select_category():
        print("select category : ")
        for index, name in enumerate(Transaction.categories, 1):
            print(f"{index}.{name}")
        while True:
            try:
                choice = int(input("Enter The category id : "))
                if 1 <= choice <= len(Transaction.categories):
                    return Transaction.categories[choice - 1]
            except ValueError:
                print("invalid id , try again")
                
    def add_transcation(self, username , amount, category, date, recurring):
        new_transaction = {
            "amount" : amount,
            "category" : category,
            "date" : date,
            "recurring" : recurring,
            "username" : username
        }
        
        # open the json 
        try : 
            with open('data/Transactions.json' , 'r') as transactionfile:
                transactions = json.load(transactionfile)
        except (json.JSONDecodeError):
            transactions = []
        
        # add it to the json file 
        transactions.append(new_transaction)
        
        # write it to the json file 
        with open('data/Transactions.json' , 'w') as file:
            json.dump(transactions , file , indent=4)
        
        print("transation Added ! ")