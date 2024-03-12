'''
Create a BankAccount dataclass that has all the needed properties
Create a BankAccountManager class that holds a list of all BankAccount instances created and performs all the appropriate operations on them
For now, skip handling the TRANSFER operation
For debugging, log the string representation of each account before and after the bank command action was taken.
'''
import logging
from conversion import CurrencyConversion


logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s. Command: %(command)s, Parameters: %('
                                                'parameters)s', datefmt='%Y-%m-%d %H:%M:%S,%')


class BankAccount:
    def __init__(self, acc_id: str, owner_name: str, currency: str):
        self.acc_id = acc_id
        self.owner_name = owner_name
        self.currency = currency
        self.balance = 0


class BankAccountManager(BankAccount):

    @classmethod
    def create_acc(cls, acc_id, owner_name, currency, balance=0):
        with open('bank-records.txt', 'a') as file:
            file.write(f'CREATE_ACC "{owner_name}" {balance} {currency}\n')
        new_account = BankAccount(acc_id, owner_name, currency)
        new_account.balance = balance
        logging.debug('Created new account')
        return new_account

    def deposit(self, amount):
        with open('bank-records.txt', 'a') as file:
            file.write(f'DEPOSIT {self.acc_id} {amount}\n')
        self.balance += amount
        logging.debug('Deposited %s %s into account %s', amount, self.currency, self.acc_id)

    def withdraw(self, amount):
        if amount <= 0:
            print('Invalid withdrawal amount')
            return
        if self.balance < amount:
            print('Insufficient funds')
            return
        with open('bank-records.txt', 'a') as file:
            file.write(f'WITHDRAW {self.acc_id} {amount}\n')
        self.balance -= amount
        logging.debug('Withdrawn %s %s from account %s', amount, self.currency, self.id)

    @staticmethod
    def transfer(acc1, acc2, amount):
        if amount <= 0:
            print('Invalid transfer amount')
            return

        if acc1.currency != acc2.currency:
            conversion = CurrencyConversion()
            converted_amount = conversion.convert_currency(amount, acc1.currency, acc2.currency)
            if converted_amount is None:
                print('Currency conversion not supported')
                return
            acc1.balance -= amount
            acc2.balance += converted_amount
        else:
            acc1.balance -= amount
            acc2.balance += amount
        with open('bank-records.txt', 'a') as file:
            file.write(f'TRANSFER {acc1.acc_id} {acc2.acc_id} {amount}\n')
        logging.debug('Transferred %s %s from account %s to account %s', amount, acc1.currency, acc1.acc_id, acc2.acc_id)

    def delete_acc(self):
        with open('bank-records.txt', 'a') as file:
            file.write(f'DELETE_ACC {self.acc_id}\n')
        logging.debug('Deleted account %s', self.acc_id)
        del self

    def dump_accounts_to_csv(self):
        pass