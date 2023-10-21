import requests
from bs4 import BeautifulSoup
import sqlite3


import time

with open('destination.txt', 'w') as f:
    f.write('')



class Parcing:
    def create_database(self, scrabing_attr, details):
        self.db = sqlite3.connect(details['db_name'])
        self.cursor = self.db.cursor()
        self.table_name = details['table_name']

        order = f"CREATE TABLE {self.table_name} ( id INTEGER PRIMARY KEY AUTOINCREMENT, link TEXT,"
        for parcing_object in scrabing_attr:
            order += ' ' + parcing_object['name'] + ' ' + 'TEXT,'
        order = order[:-1]
        order += ')'

        self.cursor.execute(order)
        self.db.commit()

    def create_order(self, parsed_info_dict):
        names = '('
        asks = '('
        for name, value in parsed_info_dict.items():
            names += ' ' + name + ','
            asks += '?,'
        names = names[:-1]
        asks = asks[:-1]
        names += ')'
        asks += ')'
        order = "INSERT INTO " + self.table_name + ' ' + names + ' VALUES ' + asks + ';'
        return order

    def count_pages(self, html_page, pagination_attr):
        soup = BeautifulSoup(html_page, 'html.parser')
        pagination_list = soup.find(pagination_attr['attribute'], attrs={'class': pagination_attr['html_class']})
        pagination = pagination_list.find_all('li')
        if pagination[len(pagination) - 1].text.isnumeric():
            return int(pagination[len(pagination) - 1].text)
        else:
            return int(pagination[len(pagination) - 2].text)


    def scrabing(self, scrabing_attr, details, links=None, create_table=True):
        if create_table:
            self.create_database(scrabing_attr, details)
        if links == None:
            with open(details['source'], 'r') as s:
                links = s.read().split('\n')
        for link in links:
            response = requests.get(link)
            original_soup = BeautifulSoup(response.text, 'html.parser')
            parsed_info_dict = {}
            for block in scrabing_attr:
                soup = original_soup
                for path in block['path']:
                    if path['place'] == 0:
                        soup = soup.find(path['attribute'], attrs={
                            'class': path['html_class']})
                    else:
                        soup = soup.find_all(path['attribute'], attrs={
                            'class': path['html_class']})
                        soup = soup[path['place']]

                parsed_info_dict[block['name']] = soup.text.strip()
            parsed_info_dict['link'] = link
            self.cursor.execute(self.create_order(parsed_info_dict), tuple(parsed_info_dict.values()))
            self.db.commit()


    def title_scrabing(self, source_attr, scrabing_attr, details, source_urls=None, create_table=True):
        if create_table:
            self.create_database(scrabing_attr, details)
        if source_urls == None:
            with open(details['source'], 'r') as s:
                source_urls = s.read().split('\n')
        for source_url in source_urls:
            response = requests.get(source_url)
            soup = BeautifulSoup(response.text, 'html.parser')
            #print(source_url, source_attr)
            all_titles = soup.find_all(source_attr['attribute'], attrs={'class': source_attr['html_class']})
            for title in all_titles:
                #print(title.text)
                link_attr = title.find('a')
                link = link_attr.attrs['href']
                if link.startswith('http'):
                    pass
                elif link.startswith('/'):
                    link = details['domain'] + link
                else:
                    link = details['domain'] + '/' + link
                try:
                    self.scrabing(scrabing_attr, details, [link], create_table=False)
                except:
                    print('except!')
                    continue


    def super_scrabing(self, pagination_attr, source_attr, scrabing_attr, details):
        self.create_database(scrabing_attr, details)
        url = details['source']
        url_arr = url.split('%%')
        response = requests.get(url_arr[0] + '1' + url_arr[1])
        pages = self.count_pages(response.text, pagination_attr)
        for page in range(1, pages + 1):
            print('page: ', page, '/', pages)
            source_url = url_arr[0] + str(page) + url_arr[1]
            self.title_scrabing(source_attr, scrabing_attr, details, [source_url], create_table=False)



scrabing_attr = [
    {'name': 'car_name', 'path': [{'attribute': 'span', 'html_class': 'vehicle-title-text', 'place': 0,}]},
    {'name': 'car_color', 'path': [{'attribute': 'div', 'html_class': 'vehicle-details-info', 'place': 0,},
                               {'attribute': 'table', 'html_class': '', 'place': 0,},
                               {'attribute': 'tbody', 'html_class': '', 'place': 0,},
                               {'attribute': 'tr', 'html_class': '', 'place': 4,},
                               {'attribute': 'td', 'html_class': '', 'place': 1,}]},
]

source_attr = [{'attribute': 'td', 'html_class': 'vehicle-description'}]


pagination_attr = [{'attribute': 'ul', 'html_class': 'pagination'}]

details = {
    'source': 'https://nordauto.ee/en/cars-catalog/?listing_page=%%',
    'domain': 'https://nordauto.ee',
    'db_name': 'parcedInfo.db',
    'table_name': 'nordauto',
}



#print(super_scrabing(pagination_attr, source_attr, scrabing_attr, details))
parcing = Parcing()
parcing.super_scrabing(pagination_attr, source_attr, scrabing_attr, details)