import os
import numpy as np
import json
import re


def remove_regex_from_string(string, chars):

    return re.sub(chars, "", string)


def read_file(filename):
    f = open(filename, 'r').read().split("\n")
    cards = [card.split("-") for card in f[:-1]]
    return cards


def name_to_url_part(cardName):
    card = cardName
    chars_to_remove = ",|:|'|// "

    card = remove_regex_from_string(card, chars_to_remove)

    card = "-".join(card.split(" "))

    return card


def read_set_cards(filename):
    # Cards are read assuming that the JSON comes from:
    # https://mtgjson.com/changelog/mtgjson-v5/

    data = json.load(open(filename))
    cards = data['data']['cards']
    cards = [[a['name'], a['rarity']]
             for a in cards if 'boosterTypes' in a.keys() and a['boosterTypes'] == ['draft']]

    unique_cards = []
    # This is not optimal.
    # Made due to how the JSON is generated
    # Cards are repeated if they are double faced
    for name,rarity in cards:
        previously = False
        for other_name,_ in cards:
            if name in other_name and name != other_name:
                previously = True
                break
        if not previously:
            unique_cards.append([name, rarity])
            

    return unique_cards


#print(name_to_url_part("Phyrexian Dragon Engine // Mishra, Lost to Phyrexia"))
# read_set_cards("set-json/BRO.json")
