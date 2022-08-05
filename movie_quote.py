import requests
from bs4 import BeautifulSoup

def moviequote():
    url = "http://randommovielines.herokuapp.com/randomlines"

    content = requests.get(url).content

    soup = BeautifulSoup(content, 'html.parser')

    p = list(soup.find_all('p'))
    return p[1].text
