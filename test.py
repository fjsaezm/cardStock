
from bs4 import BeautifulSoup
import numpy as np
import requests
from datetime import datetime
import pickle
import pandas as pd
import os
from tqdm import tqdm
import emoji
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

    # Check case where no Price Trend is shown:
    if len(data[0]) > 2:
        data[0] = data[1]
        data[1] = data[2]
        data[2] = ["0,0 €"]
    
    # Num units already number
    data[0] = int(data[0][0])
    for i,d in enumerate(data[1:]):
        # Preprocess output from the contents <span>NUMBER € </span>
        d = str(d[0]).replace('<span>',"")
        d = d.replace('</span>',"")
        # Check case where no data for trends
        if d != 'N/A':
            d = float(d[:-2].replace(',','.'))
        else:
            d = 0.0
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

def get_needed_emoji(first,second):
    if first > second:
        return "up_arrow"
    elif first == second:
        return "stop_button"
    else:
        return "down_arrow"

def check_price_change(cardName, price = 'from'):


    data = load_data(cardName)
    col = data[price].to_numpy()
    if len(col) < 2:
        print("Not enough data to check variation")
        return

    lowest = min(col)
    current = col[-1]
    previous = col[-2]

    num_updates = 0
    for i in range(len(col)-1):
        num_updates +=1
        if col[-i-2] != current:
            previous = col[-i-2]
            break
    
    em1 = get_needed_emoji(current,lowest)
    em2 = get_needed_emoji(current,previous)

    print("Variation in: {}".format(cardName))
    print(emoji.emojize("\t Current price {}".format(current)))
    print(emoji.emojize("\t Last price    {} :{}:".format(previous, em2)))
    print(emoji.emojize("\t Min  price    {} :{}:".format(lowest, em1)))

    print("(Number of updates since last change: {})".format(num_updates))


print("-----------------------")

def update_data(filename = "cardList.txt"):
    cards = read_file(filename)
    print("Getting data...")
    for name, expansion in tqdm(cards):
        #print(name,expansion)
        try:
            data = get_data(name,expansion)
            save_data(name,data)

        except:
            print("Couldn't retrieve data from card:{}".format(name))

def check_all_price_changes(filename = "cardList.txt", price = 'from'):
    cards = read_file(filename)
    for name,_ in cards:
        check_price_change(name,price)


#update_data()
check_all_price_changes()