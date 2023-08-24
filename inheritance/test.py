import unittest
from inherit import Bank, Account, SavingsAccount, CurrentAccount
from unittest.mock import patch, Mock


class TestBank(unittest.TestCase):
    def setUp(self):
        self.bank = Bank()

    def test_open_account(self):
        new_account = Account(1000, 2563156)
        self.bank.open_account(new_account)
        account = self.bank._accounts[0]
        self.assertEqual(account.get_account_number(), 2563156)
        self.assertEqual(account.get_balance(), 1000)

    def test_add_account_invalid_type(self):
        with self.assertRaises(TypeError):
            self.bank.open_account({100, 562356})

    def test_update_account(self):
        saving_account = SavingsAccount(500, 568956, 1.25)
        saving_account2 = SavingsAccount(500, 568956, 1.5)
        current_account = CurrentAccount(-500, 159753, -1000)
        self.bank.open_account(saving_account)
        self.bank.open_account(saving_account2)
        self.bank.open_account(current_account)

        saving_account.add_interest = Mock(return_value=506.25)
        saving_account2.add_interest = Mock(return_value=507.5)

        with patch('builtins.print') as mock_print:
            self.bank.update()
            mock_print.assert_called_with(
                "Sending letter for account 159753: Overdraft limit exceeded.")
            saving_account.add_interest.assert_called_once()
            saving_account2.add_interest.assert_called_once()

    def test_close_account(self):
        account = Account(500, 89653)
        self.bank.open_account(account)
        message = self.bank.close_account(89653)
        failure_message = self.bank.close_account(89651)

        self.assertEqual(message, "Account 89653 closed.")
        self.assertEqual(failure_message, "Account 89651 not found.")


if __name__ == '__main__':
    unittest.main()
