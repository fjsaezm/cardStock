
import urllib.request
from bs4 import BeautifulSoup
import numpy as np

def get_soup(url):
    data = urllib.request.urlopen(url).read().decode()
    #soup it
    soup = BeautifulSoup(data,'lxml')
    return soup

def get_url(cardName):
    # Find card, remove commas
    card = cardName
    if ',' in cardName:
        card = cardName.replace(",","%2C")
    card = "+".join(card.split(" "))

    # Search URL, used to get the last reprint of the card
    url = "https://www.cardmarket.com/en/Magic/Products/Search?searchString="+card

    # Get the soup
    soup = get_soup(url)
    # Get Hrefs
    req = soup.find_all('a',href = True)
    # New split, removing comma (not in link)
    card = "-".join(cardName.replace(",","").split(" "))
    # Get the last reprint in list
    for link in req:
        l = link.get('href')
        if(l.find(card) != -1):
            url = l
            break
    # Get url
    url = "https://www.cardmarket.com"+url
    return url

def get_units(cardName):
    url = get_url(cardName)
    soup = get_soup(url)
    units = soup('dd')[4].string
    print(cardName + " : " + units)


def read_file(filename):
    f = open(filename,'r').read().split("\n")
    return f[0:len(f)-1]

cards = read_file("cardList.txt")
for c in cards:
   get_units(c)
