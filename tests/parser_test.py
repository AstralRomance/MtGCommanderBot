import json
import requests
import pytest
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

@pytest.mark.parametrize('card_name', ['Thief of Sanity', 'Mortify', 'Teferi, Hero of Dominaria'])
def test_correct_response_for_full_name(card_name):
    response = requests.post(PARSER_URL, data=json.dumps(make_parser_header(card_scg_search_form(card_name))))
    assert response.status_code == 200

@pytest.mark.parametrize('card_name', ['Thief of Sanity', 'Mortify', 'Teferi, Hero of Dominaria'])
def test_non_empty_parser_response(card_name):
    response = requests.post(PARSER_URL, data=json.dumps(make_parser_header(card_scg_search_form(card_name))))
    assert response.json()['items'] is not None

@pytest.mark.parametrize('card_info', [{'Thief of Sanity': ['$1.99', 'Guilds of Ravnica']}, {'Supreme Verdict': ['$7.99', 'Iconic Masters']}])
def test_correct_price(card_info):
    set_val = list(card_info.items())[0][1][1]
    response = requests.post(PARSER_URL, data = json.dumps(make_parser_header(card_scg_search_form(str(list(card_info.items())[0][0])))))
    assert response.json()['items'][0][set_val][0]['Near Mint'] == list(card_info.items())[0][1][0]
    