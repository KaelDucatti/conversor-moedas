import os
from pprint import pprint

import requests
from dotenv import load_dotenv

load_dotenv()


class CurrencyConverter:
    def __init__(self, api_key=None):
        self.api_key = os.getenv("API_KEY")
        if not self.api_key:
            raise ValueError(
                "API_KEY não encontrada. Verifique seu arquivo .env."
            )

    def convert(self, origin_coin, target_coin):
        if not origin_coin or not target_coin:
            raise ValueError("As cotações devem ser informadas corretamente")

        origin = origin_coin.upper()
        target = target_coin.upper()

        currency = f"{origin}-{target}"

        url = f"https://economia.awesomeapi.com.br/json/last/{currency}?token={self.api_key}"

        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()

            data = response.json()
            return data.get(f"{origin}{target}").get("bid")
        except requests.exceptions.RequestException as e:
            raise ConnectionError(f"Erro na requisição: {e}")
        except ValueError as e:
            raise ValueError(f"Erro nos dados: {e}")


if __name__ == "__main__":
    converter = CurrencyConverter()
    result = converter.convert("usd", "brl")
    pprint(result)
