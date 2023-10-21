import requests
from bs4 import BeautifulSoup

url = 'https://www.bbc.com/news'

response = requests.get(url)

soup = BeautifulSoup(response.text, 'html.parser')

headlines = soup.find_all('h3', attrs={'class': 'gs-c-promo-heading__title gel-pica-bold nw-o-link-split__text'})

for line in headlines:
    print(line.text.strip(), end='\n\n')