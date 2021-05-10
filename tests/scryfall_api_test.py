import pytest
import requests
from constants import SCRYFALL_API_URL

@pytest.mark.parametrize('card_name', [{'test_name': 'Вор рассудка', 'expected_name': 'thief of sanity'}, {'test_name': 'Mortify', 'expected_name': 'mortify'}])
def test_regular_search(card_name):
    response = requests.get(''.join((SCRYFALL_API_URL, f'/cards/named?fuzzy={card_name["test_name"].replace(" ", "+")}')))
    assert response.json()['name'].lower() == card_name['expected_name']

@pytest.mark.parametrize('card_name', [{'вор рассудка':'Thief of Sanity'}, {'Унижение': 'Mortify'}, {'ТеФеРи, ГеРоЙ ДоМиНаРиИ': 'Teferi, Hero of Dominaria'}])
def test_rus_card_scryfall_api_response(card_name):
    response = requests.get(''.join((SCRYFALL_API_URL, f'/cards/named?fuzzy={list(*card_name.items())[0].replace(" ", "+")}')))
    assert response.json()['name'].lower() == list(*card_name.items())[1].lower()

@pytest.mark.parametrize('card_name', [{'test_name': 'Вор расс', 'expected_name': 'thief of sanity'}, {'test_name': 'тефери, геро', 'expected_name': 'teferi, hero of dominaria'}])
def test_part_name(card_name):
    response = requests.get(''.join((SCRYFALL_API_URL, f'/cards/named?fuzzy={card_name["test_name"].replace(" ", "+")}')))
    assert response.json()['name'].lower() == card_name['expected_name']