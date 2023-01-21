from utils import read_file, read_set_cards
from cardPrize import get_min_price
import numpy as np


MIN_MYTHICS = 3
MAX_MYTHICS = 8

def dict_min_prices(cardList, edition):
    d = {}
    for c in cardList:
        print(c)
        d[c] = get_min_price(c,edition)


class Box():

    def __init__(self,
                edition_name : str = "",
                json_path : str = "",
                n_boosters : int = 36,
                card_list : list = None,
                preloaded_prizes : dict = None) -> None:
        
        self.edition = edition_name
        if card_list is None:
            self.cards = read_set_cards(json_path)
        else:
            self.cards = card_list

        # Set N boosters and rare/mythics of the editions
        self.n_boosters = n_boosters
        self.edition_rares = [a[0] for a in self.cards if a[1] == 'rare']
        self.edition_mythics = [a[0] for a in self.cards if a[1] == 'mythic']


        if preloaded_prizes is not None:
            self.prices = preloaded_prizes
        else:
            self.prices = dict_min_prices(self.edition_rares + self.edition_mythics, self.edition)


        self.num_mythics = np.random.randint(MIN_MYTHICS,MAX_MYTHICS)
        self.num_rares = self.n_boosters - self.num_mythics
        self.opened_mythics = np.random.choice(self.edition_mythics, self.num_mythics)
        self.opened_rares = np.random.choice(self.edition_rares, self.num_rares)
        self.opened_rare_slot = np.concatenate((self.opened_rares, self.opened_mythics))

        self.total_box_price = np.sum([self.prices[c] for c in self.opened_rare_slot])


edition_name = "The Brother's War"
json_path = "set-json/BRO.json"

print("Processing box...")
ini_box = Box(edition_name = edition_name,json_path=json_path)

print("Processed box")
print(ini_box.total_box_price)
print("Opened mythics: {}".format(ini_box.opened_mythics))

shared_cards = ini_box.cards
shared_prices = ini_box.prices

exit()

a = [Box(card_list = cards).num_mythics for j in range(0,10000)]
print(min(a))
print(max(a))
print(np.mean(a))
