from datetime import datetime

class Transaction:
    def __init__(self , amount , category , date , recurring):
        self.amount = amount
        self.category = category
        self.date = datetime.strptime(date , '%Y-%m-%d')
        self.recurring = recurring
        