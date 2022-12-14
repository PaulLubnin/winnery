import argparse
import datetime
from collections import defaultdict
from http.server import HTTPServer, SimpleHTTPRequestHandler

import pandas as pd
from jinja2 import Environment, FileSystemLoader, select_autoescape


def get_winery_age():
    """
    функция определяет подходящее окончание
    """

    founding_year = 1920
    today = datetime.datetime.now()
    winery_age = today.year - founding_year

    if 21 > winery_age > 4 or 11 <= winery_age % 100 <= 14:
        return f'уже {winery_age} лет с вами'

    if winery_age % 10 == 1:
        return f'уже {winery_age} год с вами'

    if 1 < winery_age % 10 < 5:
        return f'уже {winery_age} года с вами'

    return f'уже {winery_age} лет с вами'


def set_drinks_by_category(wines: list):
    """
    функция принмает список словарей c винами, разбивает елементы по категориям и возвращает новый словарь с ключами
    категориями и значениями из изначального словаря
    :param wines:
    :return:
    """

    categorization = defaultdict(list)

    for wine in wines:
        categorization[wine['Категория']].append(wine)

    return dict(categorization)


def main():
    """
    запуск программы
    """

    parser = argparse.ArgumentParser(description='Описание программы')
    parser.add_argument('--path_to_data_file', help='Путь к файлу с карточками вин', default='wine3.xlsx')
    args = parser.parse_args()

    wine_df = pd.read_excel(args.path_to_data_file, na_values=['nan'], keep_default_na=False).to_dict(orient='record')

    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )

    template = env.get_template('template.html')

    rendered_page = template.render(
        winery_age=get_winery_age(),
        wines_catalog=set_drinks_by_category(wine_df)
    )

    with open('index.html', 'w', encoding="utf8") as file:
        file.write(rendered_page)

    server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
    server.serve_forever()


if __name__ == '__main__':
    main()
