from utils import read_file, read_set_cards
from cardPrize import get_sell_prices
import numpy as np
import pandas as pd
from tqdm import tqdm


"""
    Make the script save the prices of the cards after each card computation

    Make the script load the csv with the prices and check if less than 1 day has passed
    Possibly add argument to force update

    Add functionality so that it also stores/computes price with avg price
"""

MIN_MYTHICS = 3
MAX_MYTHICS = 8


def dict_min_prices(cardList, edition):
    d = {}
    d_avg = {}
    for c in tqdm(cardList):
        d[c],d_avg[c] = get_sell_prices(c, edition)

    return d,d_avg


class Box():

    def __init__(self,
                 edition_name: str = "",
                 json_path: str = "",
                 n_boosters: int = 36,
                 card_list: list = None,
                 prices_csv : str = None,
                 prices_dict : dict = None,
                 prices_avg_dict : dict = None) -> None:

        self.edition = edition_name
        if card_list is None:
            self.cards = read_set_cards(json_path)
        else:
            self.cards = card_list

        # Set N boosters and rare/mythics of the editions
        self.n_boosters = n_boosters
        self.edition_rares = [a[0] for a in self.cards if a[1] == 'rare']
        self.edition_mythics = [a[0] for a in self.cards if a[1] == 'mythic']

        
        # Prices may come: from dict, from csv path or none
        if prices_dict is not None and prices_avg_dict:
            self.prices = prices_dict
            self.avg_prices = prices_avg_dict
        else:
            if prices_csv is not None:
                df = pd.read_csv(prices_csv)
                d = df.to_dict()
                # Convert to desired format
                self.prices = {d['name'][i]:d['price'][i] for i in range(len(d['name']))}
                self.avg_prices = {d['name'][i]:d['avg_price'][i] for i in range(len(d['name']))}

            else:
                self.prices, self.avg_prices = dict_min_prices(
                    self.edition_rares + self.edition_mythics, self.edition)
                # Save dict
                cols = ['name','price', 'avg_price']
                names = self.prices.keys()
                prices = self.prices.values()
                avg_prices = self.avg_prices.values()
                new_dict = {cols[0]:names, cols[1]:prices, cols[2]:avg_prices}
                df = pd.DataFrame(new_dict)
                df.to_csv("price-csv/"+edition_name+".csv")

        self.num_mythics = np.random.randint(MIN_MYTHICS, MAX_MYTHICS)
        self.num_rares = self.n_boosters - self.num_mythics
        self.opened_mythics = np.random.choice(
            self.edition_mythics, self.num_mythics)
        self.opened_rares = np.random.choice(
            self.edition_rares, self.num_rares)
        self.opened_rare_slot = np.concatenate(
            (self.opened_rares, self.opened_mythics))

        self.total_box_price = np.sum(
            [self.prices[c] for c in self.opened_rare_slot])

        self.total_box_price_avg = np.sum(
            [self.avg_prices[c] for c in self.opened_rare_slot])


edition_name = "Phyrexia: All Will Be One"
json_path = "set-json/ONE.json"
csv_path = "price-csv/" + edition_name + ".csv"

print("Processing box...")
ini_box = Box(edition_name=edition_name,json_path=json_path, prices_csv = csv_path)

print("Processed box")
print(ini_box.total_box_price)
#print("Opened mythics: {}".format(ini_box.opened_mythics))
#print("Opened rares: {}".format(ini_box.opened_rares))

print("Min total price: {}".format(ini_box.total_box_price))
print("Avg total price: {}".format(ini_box.total_box_price_avg))


shared_cards = ini_box.cards
shared_prices = ini_box.prices
shared_avg_prices = ini_box.avg_prices

boxes = [Box(edition_name = edition_name,card_list=shared_cards, prices_dict = ini_box.prices, prices_avg_dict= shared_avg_prices) for j in range(0, 10000)]

boxes_min_prices = [b.total_box_price for b in boxes]
boxes_avg_prices = [b.total_box_price_avg for b in boxes]

print("Minimum prices:")
print("\tMin: {}".format(min(boxes_min_prices)))
print("\tMax: {}".format(max(boxes_min_prices)))
print("\tAvg of min prices: {}".format(np.mean(boxes_min_prices)))


print("AVG prices:")
print("\tMin: {}".format(min(boxes_avg_prices)))
print("\tMax: {}".format(max(boxes_avg_prices)))
print("\tAvg of AVG prices: {}".format(np.mean(boxes_avg_prices)))
