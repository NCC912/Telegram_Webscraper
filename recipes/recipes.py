import requests
from bs4 import BeautifulSoup
import io

url = "http://allrecipes.com/search/results/?search="
def getContent():
    with open("search.html") as f:
        result = f.read()
    return result

def getRecipe():
    with open("recipe.html") as f:
        result = f.read()
    return result


def searchRecipe(query: str) -> str:
    query = query.replace(' ','%20')
    searchContent = BeautifulSoup(requests.get(url+query).content, 'html.parser')
    searchItems = searchContent.find_all(attrs={'role':'listitem'})
    link = searchItems[0].find('a')['href']
    return link
#requests.get(url).content
def readRecipe(url: str) -> str:
    soup = BeautifulSoup(requests.get(url).content,"html.parser")
    name = soup.find('h1',class_="headline").text
    ingredientTags = soup.find_all('span', class_="ingredients-item-name")
    ingredients = [tag.text for tag in ingredientTags]
    instructions = []
    for instruction in soup.find('ul',class_="instructions-section").find_all('li'):
        instructions.append(instruction.find('div',class_="paragraph").text)
    return name, ingredients, instructions

def recipe(query):
    result = ""
    url = searchRecipe(query)
    name, ingredients, instructions = readRecipe(url)
    result += "How to make: "+name+"\n"
    result += "You will need:\n"
    for item in ingredients:
        result+="   "+item+"\n"
    result += "To make it you need to:\n"
    for i, instruction in enumerate(instructions):
        result += "   "+str(i+1)+": "+instruction+"\n"
    return result
if __file__ == "__main__":
    query = input("What would you like to make?")
    recipe(query)
