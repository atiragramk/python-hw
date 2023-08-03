from inherit import (
    Book,
    FastFood,
    CurrentAccount,
    SavingsAccount,
    Account,
    Bank
)


if __name__ == "__main__":
    dark_tower = Book("The Dark Tower", 20.5, 30, "Stephen King")
    dark_tower.read()

    menu = {
        'burger': {'price': 5, 'quantity': 10},
        'pizza': {'price': 10, 'quantity': 20},
        'drink': {'price': 1, 'quantity': 15}
    }

    mc = FastFood('McDonalds', 'Fast Food', menu, True)

    print(mc.order('burger', 5))  # 25
    print(mc.order('burger', 15))  # Requested quantity not available
    print(mc.order('soup', 5))  # Dish not available

    print(mc.menu)

    normal_acc = Account(2500, 2563156)
    curr_acc = CurrentAccount(2000, 562358456, 500)
    sav_acc = SavingsAccount(5250, 265489653, 1.25)

    bank = Bank()

    bank.open_account(normal_acc)
    bank.open_account(curr_acc)
    bank.open_account(sav_acc)

    for account in bank._accounts:
        print(account.get_balance())

    bank.pay_dividend(100)
    bank.update()

    for account in bank._accounts:
        print(account.get_balance())

    bank.close_account(265489653)
    print(bank._accounts)
