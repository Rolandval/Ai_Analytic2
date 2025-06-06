import requests

def get_currency_rate(ccy: str = "USD") -> dict:
    """
    Отримати курс валюти до гривні з API ПриватБанку.

    :param ccy: Код валюти (наприклад: "USD", "EUR")
    :return: Словник з курсом купівлі та продажу, або None якщо валюта не знайдена
    """
    url = "https://api.privatbank.ua/p24api/pubinfo?json&exchange&coursid=5"
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()
        for item in data:
            if item["ccy"] == ccy.upper():
                return {
                    "currency": ccy.upper(),
                    "rate": item["buy"],
                }
        return None
    except requests.RequestException as e:
        print(f"Помилка при запиті: {e}")
        return None


if __name__ == "__main__":
    print(get_currency_rate("USD"))