import json
import requests
from constants import PARSER_URL, STARCITY_SEARCH

def make_parser_header(card_name):
    price_parsing = {
                        'request':
                        {
                            'url':card_name,
                            'dont_filter':True
                        },
                       'spider_name':'starcitygames'
                    }
    return price_parsing

def card_scg_search_form(card: str) -> str:
    card = card.replace(' ', r'%20').replace(',',r'%25c%25')
    return ''.join((STARCITY_SEARCH,card))

def server_test():
    for _ in range(1000):
        get_random_card = requests.get('https://api.scryfall.com/cards/random')
        random_card_prepare = card_scg_search_form(get_random_card.json()['name'])
        response = requests.post(PARSER_URL, data=json.dumps(make_parser_header(random_card_prepare)))


server_test()