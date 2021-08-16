import asyncio
from pathlib import Path
import sqlite3
import requests
from requests import models.Response
import json


from tg_bot import URL_CONSTANTS


class DataCollector:
    def __init__(self):
        self.db_path = Path('ScryfallDataBase.db')

    # async def card_search(self):
    #     pass

    async def card_search(card_names: list) -> tuple:
        for card in card_names:
            card.replace('//','+')
            card_request_string = f'https://api.scryfall.com/cards/named?fuzzy={card.replace(" ","+")}'
            card_request = requests.get(card_request_string)
            card_json = card_request.json()
            try:
                eng_card_name = card_json['name']
            except KeyError as eng_name_key_error:
                with open('logs/logs.log', 'a') as log_file:
                    log_file.write(card_json['scryfall_uri'])
            if 'set' in card_json:
                set_name = card_json['set']
                card_number = card_json['collector_number']
            rus_card_link = f'http://api.scryfall.com/cards/{set_name}/{card_number}/ru'
            rus_card_request = requests.get(rus_card_link)
            rus_card_json = rus_card_request.json()
            if rus_card_request.status_code == 404:
                rus_card_name = '-'
            else:
                if 'printed_name' in rus_card_json:
                    rus_card_name = rus_card_json['printed_name']
                # For cards with two parts
                else:
                    rus_card_name = rus_card_json['card_faces'][0]['printed_name'] + ' // ' + rus_card_json['card_faces'][1]['printed_name']
            # Error on card 'R&D's Secret Lair '
            if 'image_uris' in card_json:
                card_image = card_json['image_uris']['normal']
            else:
                card_image = card_json['card_faces'][0]['image_uris']['normal']
            return await (eng_card_name, rus_card_name, card_image )
            

    async def write_to_db(data: tuple):
        cur.execute("INSERT OR IGNORE INTO cards VALUES(?,?,?);", data)
        conn.commit()

    def get_db() -> Response:
        card_names = requests.get('https://api.scryfall.com/catalog/card-names')
        return card_names
