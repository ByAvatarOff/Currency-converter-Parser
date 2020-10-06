import requests
from bs4 import BeautifulSoup


URL = 'https://www.alfabank.by/currencys/nbrb/'
HEADERS = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:78.0)', 'accept': '*/*'}


def get_html(url):
    r = requests.get(url, headers=HEADERS)
    return r


def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    test = []
    work = {}
    items = soup.find_all('div', class_='currency-price', limit=3)
    for item in items:
        test.append(float(item.get_text(strip=True).replace('\n', ' ').replace(',', '.')))
    work['1 USD'] = test[0]
    work["1 EUR"] = test[1]
    work["100 RUB"] = test[2]
    return work


def parse():
    html = get_html(URL)
    if html.status_code == 200:
        f = get_content(html.text)
    return f


def convert():
    convert_value = parse()
    while True:
        what_are_you_convert = input('Если вы хотите перевести бел.руб в другую валюту введите -, если наоборот, введите +: ')
        currency = str(input('Введите валюту (USD, EUR, RUB) в которую нужно перевести: ')).upper()
        if what_are_you_convert == '+':
            try:
                value = int(input('Введите сумму которую вы хотите перевсти в беларусские рубли: '))
            except ValueError:
                print('Введите сумму в цифрах')

            if currency == 'USD':
                bel1 = value * convert_value['1 USD']
                print('{:.2f}'.format(bel1), 'бел. руб')
            elif currency == 'EUR':
                bel2 = value * convert_value['1 EUR']
                print('{:.2f}'.format(bel2), 'бел. руб')
            elif currency == 'RUB':
                bel3 = value * convert_value['100 RUB'] / 100
                print('{:.2f}'.format(bel3), 'бел. руб')
            else:
                print('Введите корректный формат денег')
        elif what_are_you_convert == '-':
            try:
                value = int(input('Введите сумму в которую вы хотите перевсти в беларусские рубли: '))
            except ValueError:
                print('Введите сумму в цифрах')

            if currency == 'USD':
                bel1 = value / convert_value['1 USD']
                print('{:.2f}'.format(bel1), 'USD')
            elif currency == 'EUR':
                bel2 = value / convert_value['1 EUR']
                print('{:.2f}'.format(bel2), 'EUR')
            elif currency == 'RUB':
                bel3 = value * convert_value['100 RUB'] * 10
                print('{:.2f}'.format(bel3), 'RUB')
            else:
                print('Введите корректный формат денег')

        else:
            print('Введите + или -')


convert()

