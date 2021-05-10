import pytest
import requests
from constants import SCRYFALL_API_URL

@pytest.mark.parametrize('card_name', [{'вор рассудка':'Thief of Sanity'}, {'Унижение': 'Mortify'}, {'ТеФеРи, ГеРоЙ': 'Teferi, Hero of Dominaria'}])
def test_rus_card_scryfall_api_response(card_name):
    response = requests.get(''.join((SCRYFALL_API_URL, f'/cards/named?fuzzy={list(*card_name.items())[0].replace(" ", "+")}')))
    print(response.json()['name'])
    assert response.json()['name'] == list(*card_name.items())[1]
