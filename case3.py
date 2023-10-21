import requests
from bs4 import BeautifulSoup

url = 'https://www.bbc.com/news'

response = requests.get(url)

soup = BeautifulSoup(response.text, 'html.parser')

attribute = 'div'
html_class = 'gs-c-promo-image gel-1/1 gel-3/4@l gel-3/5@xxl gs-u-float-right@l'

first_div = soup.find_all(attribute, attrs={'class': html_class})
second_div = first_div[0].find('div')
thirth_div = second_div.find('div')


image = thirth_div.find('img')
#width = 240
# print(image[0].attrs['data-src'])
print(image.attrs['alt'])