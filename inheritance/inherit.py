class Product:
    def __init__(self, name: str, price: int or float, quantity: int) -> None:
        self.name = name
        self.price = price
        self.quantity = quantity


class Book(Product):
    def __init__(self, name: str, price: int, quantity: int, author: str) -> None:
        super().__init__(name, price, quantity)
        self.author = author

    def read(self):
        print(
            f'The title of book: {self.name}.\nPrice: {self.price}.\nAuthor:{self.author}\nAvailable: {self.quantity}')


class Restaurant:
    def __init__(self, name: str, cuisine: str, menu: dict) -> None:
        self.name = name
        self.cuisine = cuisine
        self.menu = menu


class FastFood(Restaurant):
    def __init__(self, name: str, cuisine: str, menu: dict, drive_thru: bool) -> None:
        super().__init__(name, cuisine, menu)
        self.drive_thru: drive_thru

    def order(self, dish_name: str, dish_quantity: int):
        if dish_name in self.menu:
            price, quantity = self.menu[dish_name].values()
            left_quantity = quantity - dish_quantity
            if left_quantity >= 0:
                self.menu[dish_name]['quantity'] = left_quantity
                return f'Total cost: {price * dish_quantity}'
            return f'We are sorry.The available quantity of {dish_name} is {quantity}'
        return f'We are sorry. The product {dish_name} is not in our menu'


class Account:
    def __init__(self, balance: int or float, account_number: int):
        self._balance = balance
        self._account_number = account_number

    @classmethod
    def create_account(cls, account_number):
        return cls(0.0, account_number)

    def deposit(self, amount):
        if amount > 0:
            self._balance += amount
        else:
            raise ValueError('Amount must be positive')

    def withdraw(self, amount):
        if amount > 0:
            self._balance -= amount
        else:
            raise ValueError('Amount must be positive')

    def get_balance(self):
        return self._balance

    def get_account_number(self):
        return self._account_number

    def __str__(self):
        return f'Account number: {self._account_number}, balance: {self._balance}'


class SavingsAccount(Account):
    def __init__(self, balance: int or float, account_number: int, interest: int or float):
        super().__init__(balance, account_number)
        self._interest = interest

    def add_interest(self):
        self._balance += round(self._balance * self._interest / 100, 2)

    def __str__(self):
        return f'{super().__str__()}, interest: {self._interest}'


class CurrentAccount(Account):
    def __init__(self, balance: int or float, account_number: int, overdraft: int):
        super().__init__(balance, account_number)
        self._overdraft = overdraft

    def withdraw(self, amount):
        self._balance -= amount + self._overdraft

    def __str__(self):
        return f'{super().__str__()}, overdraft: {self._overdraft}'


class Bank:
    def __init__(self, accounts: list[Account] = []) -> None:
        self._accounts = accounts

    def __str__(self):
        return f'Account List: {self._accounts}'

    def update(self):
        for account in self._accounts:
            if isinstance(account, CurrentAccount):
                if account._balance < 0:
                    return f"Sending letter for account {account._account_number}: Overdraft limit exceeded."
            if isinstance(account, SavingsAccount):
                account.add_interest()

    def open_account(self, account):
        if not isinstance(account, Account):
            return TypeError("The account is not the instance of needed classes")
        self._accounts.append(account)

    def close_account(self, account_number: int):
        for account in self._accounts:
            if account._account_number == account_number:
                self._accounts.remove(account)
                return f"Account {account_number} closed."
        return f"Account {account_number} not found."

    def pay_dividend(self, dividend: int):
        for account in self._accounts:
            account.deposit(dividend)
