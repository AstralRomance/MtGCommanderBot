import sqlite3 as sql
import requests
import json

def add_card(card_names):
    for i in card_names:
        i.replace('//','+')
        card_request_string = ''.join((f'http://api.scryfall.com/cards/named?fuzzy={i.replace(" ","+")}'))
        card_request = requests.get(card_request_string)
        card_json = card_request.json()
        if 'set' in card_json:
            set_name = card_json['set']
            card_number = card_json['collector_number']
        rus_card_link = ''.join((f'http://api.scryfall.com/cards/{set_name}/{card_number}/ru'))
        rus_card_request = requests.get(rus_card_link)
        rus_card_json = rus_card_request.json()
        if rus_card_request.status_code == 404:
            rus_card_name = '-'
        else:
            if 'printed_name' in rus_card_json:
                rus_card_name = rus_card_json['printed_name']
            else:
                rus_card_name = rus_card_json['card_faces'][0]['printed_name'] + ' // ' + rus_card_json['card_faces'][1]['printed_name']
        eng_card_name = card_json['name'] #Error on card 'R&D's Secret Lair '
        if 'image_uris' in card_json:
            card_image = card_json['image_uris']['normal']
        else:
            card_image = card_json['card_faces'][0]['image_uris']['normal']
        card = (eng_card_name, rus_card_name, card_image )
        cur.execute("INSERT OR IGNORE INTO cards VALUES(?,?,?);", card)
        conn.commit()

conn = sql.connect('/home/alex/Рабочий стол/DataBase/ScryfallDataBase.db') #connecting to the database
cur = conn.cursor()
resp = requests.get('https://api.scryfall.com/catalog/card-names') #getting the card names
link = ''.join('https://api.scryfall.com/catalog/card-names')
link_request = requests.get(link)
link_json = link_request.json()
add_card(link_json['data'])