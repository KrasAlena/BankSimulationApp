import csv
import logging
from dataclasses import dataclass
from typing import List
from conversion import CurrencyConversion


logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s. Command: %(command)s, Parameters: %('
                                                'parameters)s', datefmt='%Y-%m-%d %H:%M:%S,%')


@dataclass
class BankAccount:
    account_holder: str
    account_id: int
    account_balance: float
    account_currency: str


class BankAccountManager:
    def __init__(self):
        self.accounts: List[BankAccount] = []
        self.account_id = 1
        self.conversion = CurrencyConversion()

    def create_bank_account(self, account_holder: str, account_balance: float, account_currency: str):
        new_account = BankAccount(account_holder, self.account_id, account_balance, account_currency)
        self.accounts.append(new_account)
        self.account_id += 1
        return new_account

    def deposit(self, account_id: str, amount: float):
        for account in self.accounts:
            if account.account_id == account_id:
                account.account_balance += amount
                return

        logging.warning(f'This {account_id} is not available')

    def withdraw(self, account_id: str, amount: float):
        tax_withdraw = amount * 0.005
        for account in self.accounts:
            if account.account_id == account_id:
                if account.account_balance >= amount + tax_withdraw:
                    account.account_balance -= amount
                    account.account_balance -= tax_withdraw
                    return
                else:
                    logging.warning(f'You are trying to withdraw more than you have')
                    return

        logging.warning(f'This {account_id} is not available')

    def transfer(self, from_account_id: int, to_account_id: int, amount: float) -> object:
        from_account = self.get_account_by_id(from_account_id)
        to_account = self.get_account_by_id(to_account_id)
        if from_account and to_account:
            if from_account.account_currency != to_account.account_currency:
                converted_amount = self.conversion.convert_currency(amount, from_account.account_currency,
                                                               to_account.account_currency)
                if converted_amount is None:
                    logging.warning('Currency conversion not supported')
                    return
                from_account.account_balance -= amount
                to_account.account_balance += converted_amount
            else:
                from_account.account_balance -= amount
                to_account.account_balance += amount
            logging.debug(
                f'Transferred {amount} from account {from_account_id} to account {to_account_id}')
        else:
            logging.warning('One or both of the accounts specified in the TRANSFER command do not exist')

    def delete_acc(self, account_id: int):
        for account in self.accounts:
            if account.account_id == account_id:
                self.accounts.remove(account)
                logging.info(f'Account with id {account_id} deleted successfully.')
                return
        logging.warning(f'Account with id {account_id} not found.')

    def get_account_by_id(self, account_id):
        for account in self.accounts:
            if account.account_id == account_id:
                return account
        return None

    def process_records(self, records: list):
        for record in records:
            command = record[0]
            if command == 'CREATE_ACC':
                _, owner_name, balance, currency = record
                self.create_bank_account(owner_name, float(balance), currency)
            elif command == 'DEPOSIT':
                _, account_id, amount = record
                self.deposit(account_id, float(amount))
            elif command == 'WITHDRAW':
                _, account_id, amount = record
                self.withdraw(account_id, float(amount))
            elif command == 'DELETE_ACC':
                _, account_id = record
                self.delete_acc(account_id)
            elif command == 'TRANSFER':
                _, from_account_id, to_account_id, amount = record
                self.transfer(from_account_id, to_account_id, float(amount))

def main():
    account_manager = BankAccountManager()

    acc1 = account_manager.create_bank_account('Alice', 100, 'EUR')
    acc2 = account_manager.create_bank_account('Bob', 50, 'USD')

    # Transfer funds from acc1 to acc2
    account_manager.transfer(acc1.account_id, acc2.account_id, 30)

    # Check the balances after the transfer
    print(f'Balance of {acc1.account_holder}: {acc1.account_balance} {acc1.account_currency}')
    print(f'Balance of {acc2.account_holder}: {acc2.account_balance} {acc2.account_currency}')


if __name__ == '__main__':
    main()