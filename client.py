import os

import requests
from dotenv import load_dotenv

load_dotenv()


class CurrencyConverter:
    def __init__(self, api_key=None):
        self.__base_url = "https://economia.awesomeapi.com.br/json/last/"
        self.__api_key = os.getenv("API_KEY")
        self.__callmebot = "http://api.callmebot.com/text.php?source=web&"
        if not self.__api_key:
            raise ValueError(
                "API_KEY não encontrada. Verifique seu arquivo .env."
            )

    def convert(self, origin_coin, target_coin):
        if not origin_coin or not target_coin:
            raise ValueError("As cotações devem ser informadas corretamente.")

        origin = origin_coin.upper()
        target = target_coin.upper()

        currency = f"{origin}-{target}"

        url = f"{self.__base_url}{currency}?token={self.__api_key}"

        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()

            data = response.json()

            currency_key = f"{origin}{target}"
            currency_data = data.get(currency_key)

            currency_bid = currency_data.get("bid")

            output = round(float(currency_bid), 2)

            return f"1 {origin} = {output} {target}"
        except requests.exceptions.RequestException as e:
            raise ConnectionError(f"Erro na requisição: {e}")
        except AttributeError as e:
            raise AttributeError(f"Erro na requisição: {e}")
        except ValueError as e:
            raise ValueError(f"Erro nos dados: {e}")

    def send_to_user(self, user, message):
        url = f"{self.__callmebot}user=@{user}&text={message}"

        try:
            response = requests.get(url)

            if response.status_code == 200:
                return "Mensagem enviada!"
            else:
                return f"Erro: {response.status_code}"
        except Exception as e:
            raise Exception(f"Erro: {e}")
