import re
import logging
from datetime import datetime


logging.basicConfig(level=logging.DEBUG)

def parse_txt():
    with open('bank-records.txt', 'r') as file:
        for line in file:
            record = line.strip()
            pattern = r'("[^"]+"|\S+)'

            new_record = re.findall(pattern, record)
            new_record = [rec.replace('"', '') for rec in new_record]

            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S,%f')[:-3]
            logging.debug('%s Command: %s, Parameters: %s', timestamp, [0], new_record[1:])

            print(new_record)

parse_txt()

