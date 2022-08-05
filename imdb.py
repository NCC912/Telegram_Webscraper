import requests
from bs4 import BeautifulSoup

search_url = "https://www.imdb.com/find?q="
base_url = "https://www.imdb.com"

def getLink(query):
    soup = BeautifulSoup(requests.get(search_url+query.replace(" ","+")+"&s=tt&ttype=ft&ref_=fn_ft").content,'html.parser')
    search_table = soup.find('table', class_="findList")
    link = search_table.find('a')['href']
    return base_url+link

def getData(url):
    soup = BeautifulSoup(requests.get(url).content,'html.parser')

    name = soup.find('h1',attrs={'data-testid':'hero-title-block__title'}).text
    infoTag = soup.find('ul',attrs={'data-testid':'hero-title-block__metadata'}).find_all("li")
    year = infoTag[0].a.text
    maturity = infoTag[1].a.text
    runtime = infoTag[2].text
    info = (year, maturity, runtime)
    rating = soup.find('div',attrs={'data-testid':'hero-rating-bar__aggregate-rating__score'}).text
    summary = soup.find('span',attrs={'data-testid':'plot-l'}).text
    return name, info, rating, summary

def lookup(query):
    url = getLink(query)
    name, (year,maturity,runtime), rating, summary = getData(url)
    result = f"Title: {name} ({year}) - {rating}\n"
    result += f"Rated {maturity}. Runtime: {runtime}\n"
    result += f"Summary: {summary}"
    return result
