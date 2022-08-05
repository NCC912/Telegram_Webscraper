# draft one

import requests
from bs4 import BeautifulSoup



#-----------UNCOMMNENT LATER

def priceList(toSearch: str):
    theSite = "https://www.ebay.com/sch/i.html?_from=R40&_trksid=m570.l1313&_nkw=" + toSearch 
    url = theSite
    content = requests.get(url).content
    soup = BeautifulSoup(content, 'html.parser')

    prices = soup.find_all("span",class_="s-item__price")
    return [item.text for item in prices]

#tempSearch= "bike"

#theSite = "https://www.ebay.com/sch/i.html?_from=R40&_trksid=m570.l1313&_nkw=" + tempSearch

#url = theSite
#content = requests.get(url).content
#soup = BeautifulSoup(content, 'html.parser')

#prices = soup.find_all("span",class_="s-item__price")
#return [item.text for item in prices]


#print(returns)








 
 














