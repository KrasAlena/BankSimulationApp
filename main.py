from bank_records import parse_txt
from accounts import BankAccountManager

def main():
    records = parse_txt('bank-records.txt')

    manager = BankAccountManager()
    print(records)
    # manager.process_commands(commands)

if __name__ == '__main__':
    main()