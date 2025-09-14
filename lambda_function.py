import json
import os

import requests


class CurrencyConverter:
    def __init__(self, api_key=None):
        self.__base_url = "https://economia.awesomeapi.com.br/json/last/"
        # Mudança: usar os.environ em vez de dotenv
        self.__api_key = os.environ.get("API_KEY")
        self.__callmebot = "http://api.callmebot.com/text.php?source=web&"
        if not self.__api_key:
            raise ValueError(
                "API_KEY não encontrada. Verifique as variáveis de ambiente do Lambda."
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


def lambda_handler(event, context):
    """
    Esta função substitui seu main.py e roda no Lambda
    """
    try:
        print("🚀 Iniciando execução do Currency Bot...")

        converter = CurrencyConverter()
        message = converter.convert("BTC", "USD")
        notification = converter.send_to_user(
            user=os.environ.get("CALLMEBOT_USER"), message=message
        )

        print(f"💰 Cotação: {message}")
        print(f"📱 Notificação: {notification}")

        return {
            "statusCode": 200,
            "body": json.dumps(
                {
                    "cotacao": message,
                    "status_envio": notification,
                    "success": True,
                }
            ),
        }

    except Exception as e:
        print(f"❌ Erro: {str(e)}")
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e), "success": False}),
        }
