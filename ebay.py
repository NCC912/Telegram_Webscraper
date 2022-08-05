# draft one

import requests
from bs4 import BeautifulSoup

def priceList(toSearch: str):
    theSite = "https://www.ebay.com/sch/i.html?_from=R40&_trksid=m570.l1313&_nkw=" + toSearch.replace(" ","+")
    url = theSite
    content = requests.get(url).content
    soup = BeautifulSoup(content, 'html.parser')

    prices = soup.find_all("span",class_="s-item__price")
    return "Prices: "+", ".join([item.text for item in prices])
