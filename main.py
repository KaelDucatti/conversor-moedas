from pprint import pprint

from client import CurrencyConverter

if __name__ == "__main__":
    converter = CurrencyConverter()
    result = converter.convert("usd", "brl")
    pprint(result)
