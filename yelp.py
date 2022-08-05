'''
Webscraping program used by the Yelp bot (see bot_info.py)
'''

import requests
from bs4 import BeautifulSoup

def search_yelp(search, city, state, zip=None):
    lin = 'https://www.yelp.com/search?find_desc={search}&find_loc={city}%2C+{state}'.format(search = search.replace(" ", "+"), city = city.replace(" ", "+"), state = state)
    print(lin)
    if zip:
        lin += "+%s" % (zip) 

    page = requests.get(lin)
    #print(page.status_code)
    soup = BeautifulSoup(page.content, 'html.parser')
    results = soup.find_all('span', class_="css-1egxyvc")
    stores = []
    links = []
    for opt in results:
        info = opt.find('a')
        if info is None:
            continue
        stores.append(info['name'])
        links.append(info)
    return (stores, links)

def find_hours(stores, links, selection):
    go_to = stores[int(selection) - 1]
    for link in links:
        if link['name'] == go_to:
            url = link['href']
            break
    storefront = requests.get("https://www.yelp.com%s" % str(url))
    food = BeautifulSoup(storefront.content, 'html.parser')
    data = food.find_all('span', class_='css-1fdy0l5')
    return data[len(data) - 1].text
