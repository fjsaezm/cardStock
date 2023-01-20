
from bs4 import BeautifulSoup
import numpy as np
import requests
from selenium import webdriver
from datetime import datetime
import pickle
import pandas as pd
import os
# URL Example:
# https://www.cardmarket.com/en/Magic/Products/Singles/Phyrexia-All-Will-Be-One/Minor-Misstep?language=1&minCondition=2
BASE_URL = "https://www.cardmarket.com/en/Magic/Products/Singles/{}/{}?language=1&minCondition=2"
SAVE_DIR = "data/"
#Copies, From, Trend, 30 days trend,7 days trend, day trend
COLS = ["copies","from","trend","30days","7days","day","date"]


def name_to_url_part(cardName):
    card = cardName
    if ',' in cardName:
        card = cardName.replace(",","")
    if ':' in card:
        card = cardName.replace(":","")

    card = "-".join(card.split(" "))

    return card

def get_soup(url):
    data = requests.get(url)
    #soup it
    soup = BeautifulSoup(data.content,'html.parser')
    return soup

def get_data(cardname, edition):
    card = name_to_url_part(cardname)
    edition = name_to_url_part(edition)
    url = BASE_URL.format(edition,card)
    soup = get_soup(url)
    Prices_uncut = soup.find_all("dd", class_="col-6 col-xl-7")
    
    # Data: Copies, From, Trend, 30 days trend,7 days trend, day trend
    data = [a.contents for a in Prices_uncut[-6:]]
    print(data)
    data[0] = int(data[0][0])
    for i,d in enumerate(data[1:]):
        d = str(d[0]).replace('<span>',"")
        d = d.replace('</span>',"")
        d = float(d[:-2].replace(',','.'))
        data[i+1] = d

    date = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    data.append(date)

    return data

def read_file(filename):
    f = open(filename,'r').read().split("\n")
    cards = [card.split("-") for card in f[:-1]]
    return cards

def save_data(cardName, data):
    path = SAVE_DIR + name_to_url_part(cardName)+'.pkl'
    df = None

    if os.path.exists(path):
        df = pickle.load(open(path,'rb'))
    else:
        print("Non existent, creating dataframe")
        df = pd.DataFrame(columns=COLS)

    df.loc[len(df.index)] = data

    pickle.dump(df, open(path, 'wb+'))


def load_data(cardName):
    path = SAVE_DIR + name_to_url_part(cardName)+'.pkl'
    with open(path,'rb') as f:
        return pickle.load(f)



#print(read_file('cardList.txt'))
#exit()
data = get_data("Minor Misstep", "Phyrexia: All Will Be One")
save_data("Minor Misstep", data)
d = load_data("Minor Misstep")
print(d)

cards = read_file("cardList.txt")
for name, expansion in cards:
    #print(name,expansion)
    save_data(name, get_data(name,expansion))
    print(load_data(name))
