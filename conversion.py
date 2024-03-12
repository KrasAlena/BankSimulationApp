'''
Create a conversion.py file and keep the currency conversion-related things here
Create a CurrencyConversion class which
Has a dictionary with currencies (in our example it's enough to have EUR, USD, GBP) and their conversion rates. Use the following conversion rates:
USD to EUR: 0.91
EUR to USD: 1.09
USD to GBP: 0.78
GBP to USD: 1.28
EUR to GBP: 0.85
GBP to EUR: 1.17
Has a method convert_currency that converts a given amount of one currency to a different currency
Implement the TRANSFER command handling using the CurrencyConversion class instance
'''
class CurrencyConversion:
    def __init__(self):
        self.conversion_rates = {
            'USD': {'EUR': 0.91, 'GBP': 0.78},
            'EUR': {'USD': 1.09, 'GBP': 0.85},
            'GBP': {'USD': 1.28, 'EUR': 1.17}
        }

    def convert_currency(self, amount, from_currency, to_currency):
        if from_currency not in self.conversion_rates or to_currency not in self.conversion_rates[from_currency]:
            print('Conversion not supported for given currencies')
            return None
        rate = self.conversion_rates[from_currency][to_currency]
        return amount * rate