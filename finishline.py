from bs4 import BeautifulSoup
import requests

# HTML From File
#with open("index.html", "r") as f:
#        doc = BeautifulSoup(f, "html.parser")
#
#tags = doc.find_all("p")[0]
#
#print(tags.find_all("b"))
#
url = "https://www.finishline.com/store/men/shoes/casual/_/store/product/mens-nike-air-force-1-low-casual-shoes/prod795980?styleId=CW2288&colorId=111"
def finishline():
    result = requests.get(url)
    doc = BeautifulSoup(result.text, "html.parser")
    prices = doc.find_all(text="$")
    parent = prices[0].parent
    strong = parent.find("strong")
    return strong.string
