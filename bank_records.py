import csv
import logging

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')


def parse_txt(path_to_records: str) -> list:
    bank_records = []

    with open(path_to_records, newline='') as bank_rec:
        csv_reader = csv.reader(bank_rec, delimiter=" ")

        for row in csv_reader:
            logging.debug(f'Command: {row[0]}, Parameters: {row[1:]}')
            bank_records.append(row)

    return bank_records




