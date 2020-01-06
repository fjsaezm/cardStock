
import urllib.request
from bs4 import BeautifulSoup

def get_soup(url):
    data = urllib.request.urlopen(url).read().decode()
    #soup it
    soup = BeautifulSoup(data,'lxml')
    return soup

def get_url(cardName):
    # Find card
    card = "+".join(cardName.split(" "))
    url = "https://www.cardmarket.com/en/Magic/Products/Search?searchString="+card

    soup = get_soup(url)
    # Get Hrefs
    req = soup.find_all('a',href = True)
    # New split
    card = "-".join(cardName.split(" "))
    for link in req:
        l = link.get('href')
        if(l.find(card) != -1):
            url = l
            break

    url = "https://www.cardmarket.com"+url
    return url

def get_units(cardName):
    url = get_url(cardName)
    soup = get_soup(url)
    units = soup('dd')[4].string
    print(cardName + " : " + units)

get_units("Steam Vents")
