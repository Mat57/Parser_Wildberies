from bs4 import BeautifulSoup as bs
import requests
import csv
from search_categories import ua

headers = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "user-agent": ua.random
}


def get_count_page(url):
    response = requests.get(url=url, headers=headers)
    soup = bs(response.text, 'html.parser')
    main_block = soup.find_all('a', class_='pagination-item pagination__item')
    number_of_pages = int(main_block[-1].text)
    return number_of_pages


def save_to_csv(cards):
    with open('data.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(('Первая цена', 'Вторая цена', 'Фирма', 'Тип'))

        for card in cards:
            writer.writerow((card['first_coast'], card['second_coast'], card['company'], card['type']))


def get_data_from_page(number_of_page, url):
    list_cards = []
    number_of_page = 2
    for i in range(1, number_of_page + 1):
        new_url = url + '?page=' + str(i)
        response = requests.get(url=new_url, headers=headers)
        soup = bs(response.text, 'html.parser')
        cards = soup.find_all('div', class_='product-card j-card-item')
        for card in cards:
            try:
                card_dict = {}
                try:
                    first_coast = \
                        card.find('span', class_='price-commission__price').text.replace('\n', '').replace(' ',
                                                                                                           '').split(
                            '₽')[
                            0]
                except:
                    first_coat = card.find('span', class_="price").text.split()[0]
                try:
                    second_coast = \
                        card.find('span', class_='price-commission__price').text.replace('\n', '').replace(' ',
                                                                                                           '').split(
                            '₽')[
                            1]
                except:
                    second_coast = card.find('span', class_="price").text.split()[0]
                company = card.find('div', class_="product-card__brand-name").text.replace('\n', '').split('/')[0]
                type = card.find('div', class_="product-card__brand-name").text.replace('\n', '').split('/')[1]
                card_dict['first_coast'] = first_coast
                card_dict['second_coast'] = second_coast
                card_dict['company'] = company
                card_dict['type'] = type
                list_cards.append(card_dict)
            except:
                pass
    save_to_csv(list_cards)


if __name__ == '__main__':
    url = str(input('Добавьте ссылку на категорию:')).replace('\n', '')
    number_of_pages = get_count_page(url)
    get_data_from_page(number_of_pages, url)
