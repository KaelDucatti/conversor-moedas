from client import CurrencyConverter

if __name__ == "__main__":
    converter = CurrencyConverter()
    message = converter.convert("BTC", "USD")
    notification = converter.send_to_user(user="@kaelducatti", message=message)
