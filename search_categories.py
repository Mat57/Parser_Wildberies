import time
from itertools import cycle
import logging
import pandas as pd
import requests
import csv
import os
from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from fake_useragent import UserAgent
import asyncio
import aiohttp
import os

ua = UserAgent()

categories = {}

path_itog = 'list_categories/itog.txt'

# proxies = {"https":"https://23.224.55.156:59394",
#            "http":"http://121.139.218.165:31409"}

black_list_category = ['Видеообзоры', 'Авиабилеты', 'Экспресс-доставка', 'Premium', 'Цифровые товары', 'Бренды',
                       'Акции', 'Товары для взрослых', 'Алкоголь']

headers = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,"
              "application/signed-exchange;v=b3;q=0.9",
    "user-agent": ua.random
}


# Создание браузера
def create_browser():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("user-agent=" + ua.random)
    driver = webdriver.Chrome(options=chrome_options, executable_path='chromedriver.exe')
    return driver


# Запись словаря в файл
def write_dict(path, dict_to_write):
    with open(path, 'w') as out:
        for key, val in dict_to_write.items():
            out.write('{}={}\n'.format(key, val))


# Получение подкатегорий
def get_sub_category():
    global categories
    logging.getLogger("main.get_sub_category")
    logger = logging.getLogger("main.get_sub_category_add")
    sub_categories = {}
    for key, val in categories.items():
        try:
            browser = create_browser()
            url = val
            browser.get(url)
            soup = browser.page_source
            res = bs(soup, 'html.parser')
            browser.close()
            if val == 'https://www.wildberries.ru/catalog/sport':
                main_block = res.find('ul', class_='menu-catalog-second__drop-list')
                sub_category = main_block.find_all('li', class_='menu-catalog-second__drop-item')
            else:
                main_block = res.find('ul', class_='menu-catalog__list-2 maincatalog-list-2')
                sub_category = main_block.find_all('li', class_='')
            for s_c in sub_category:
                sub_categories[s_c.contents[1].text] = 'https://www.wildberries.ru' + s_c.contents[1].attrs['href']
            logger.info("Подкатегории для  %s (%s)  распознаны" % (key, val))
        except:
            logger.info("Не удалось распознать подкатегории для  %s (%s) " % (key, val))
            pass
    categories = sub_categories


# Получение списка категорий: Мужчинам, Женщинам, Детям и т.п.
def get_category():
    global categories
    logging.getLogger("main.get_category")
    logger = logging.getLogger("main.get_category_add")
    url = 'https://www.wildberries.ru/'
    page = requests.get(url, headers=headers)
    try:
        if page.status_code == 200:
            html = bs(page.content, 'html.parser')
            block_with_category = html.find('div', class_='menu-burger__main j-menu-burger-main')
            list_category = block_with_category.find_all('li', class_='menu-burger__main-list-item j-menu-main-item')
            for l_c in list_category:
                if l_c.find('a').contents[0] in black_list_category:
                    pass
                else:
                    categories[l_c.find('a').contents[0]] = l_c.find('a').attrs['href']
            logger.info("Основные категории распознаны ")
        else:
            logger.info("Страница недоступна")
            print('Page unreachable')
    except:
        logger.info("Основные категории не распознаны")
        pass


# Получение подкатегорий второго уровня
def get_sub_sub_category():
    global categories
    logging.getLogger("main.get_sub_sub_category")
    logger = logging.getLogger("main.get_sub_sub_category_add")
    sub_categories = {}
    for key, val in categories.items():
        try:
            response = requests.get(url=val)
            soup = bs(response.text, "html.parser")
            main_block = soup.find('ul', class_='sidemenu')
            sub_category = main_block.find_all('ul')[0].find_all('li', class_='')
            for s_c in sub_category:
                sub_categories[key + s_c.contents[1].text] = 'https://www.wildberries.ru' + s_c.contents[1].attrs[
                    'href']
            logger.info("Подкатегории для  %s (%s)  распознаны" % (key, val))
        except:
            logger.info("Не удалось распознать подкатегории для  %s (%s) " % (key, val))
            sub_categories[key] = val
            pass
    categories = sub_categories
    if os.path.exists(path_itog):
        os.remove(path_itog)
    else:
        pass
    write_dict(path_itog, categories)


# Формирование excel
def from_txt_to_excel():
    with open('list_categories/itog.txt', 'r') as in_file:
        stripped = (line.strip() for line in in_file)
        lines = (line.split("=") for line in stripped if line)
        with open('list_categories/itog.csv', 'w', newline='') as out_file:
            writer = csv.writer(out_file, delimiter='=')
            writer.writerows(lines)


if __name__ == '__main__':
    logger = logging.getLogger("main")
    logger.setLevel(logging.INFO)
    fh = logging.FileHandler("log/cateroies.log")
    console_out = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    logger.addHandler(console_out)
    logger.info("Program started")
    get_category()
    get_sub_category()
    get_sub_sub_category()
    from_txt_to_excel()
    logger.info("Done!")
