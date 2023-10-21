import requests
from bs4 import BeautifulSoup

url = 'https://www.bbc.com/news'

response = requests.get(url)

soup = BeautifulSoup(response.text, 'html.parser')

attribute = 'div'
html_class = 'gs-o-responsive-image gs-o-responsive-image--16by9'

headlines = soup.find_all(attribute, attrs={'class': html_class})


for line in headlines:
    image = line.find_all('img')
    #width = 240
    # print(image[0].attrs['data-src'])
    print(image[0].attrs['alt'])