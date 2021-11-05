from bs4 import BeautifulSoup as bs
import requests
import csv
from search_categories import ua
import asyncio
import aiohttp

headers = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "user-agent": ua.random
}

list_cards=[]

async def get_count_page(url):
    async with aiohttp.ClientSession() as session:
        response = await session.get(url=url, headers=headers)
        resp = await response.text()
        soup = bs(resp, 'html.parser')
        main_block = soup.find_all('a', class_='pagination-item pagination__item')
        number_of_pages = int(main_block[-1].text)

        tasks = []

        for page in range(1, number_of_pages+1):
            task = asyncio.create_task(get_data_from_page(session, str(page)))
            tasks.append(task)
        await asyncio.gather(*tasks)


def save_to_csv(cards):
    with open('data.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(('Первая цена', 'Вторая цена', 'Фирма', 'Тип'))

        for card in cards:
            writer.writerow((card['first_coast'], card['second_coast'], card['company'], card['type']))


async def get_data_from_page(session, page):
    global list_cards
    new_url = url + '?page=' + str(page)
    async with session.get(url=new_url, headers=headers) as response:
        resp = await response.text()
        soup = bs(resp, 'html.parser')
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
        print(f"Обработал страницу {page}")



if __name__ == '__main__':
    url = str(input('Добавьте ссылку на категорию:')).replace('\n', '')
    asyncio.get_event_loop().run_until_complete(get_count_page(url))
    save_to_csv(list_cards)

