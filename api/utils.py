import requests

def format_int(x: int) -> str:
    return '{:,}'.format(x).replace(',', '\'')


def get_crypt_course_online() -> tuple[float, float]:
    try:
        t = requests.get('https://api.coincap.io/v2/assets?ids=bitcoin,ethereum').json()
    except requests.exceptions.RequestException:
        return 0, 0
    bitcoin, ethereum = 0, 0
    for i in t['data']:
        if i['id'] == 'bitcoin':
            bitcoin = float(i['priceUsd'])
        elif i['id'] == 'ethereum':
            ethereum = float(i['priceUsd'])
    return bitcoin, ethereum

def get_usd_course_online() -> float:
    try:
        t = requests.get('https://www.cbr-xml-daily.ru/daily_json.js').json()
    except requests.exceptions.RequestException:
        return 0
    return float(t['Valute']['USD']['Value'])

