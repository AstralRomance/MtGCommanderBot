import json
import requests

def doubleface(card_name):
    if '//' in card_name:
        print('YES')
    i = card_name
    i.replace('//','+')
    card_request_string = ''.join((f'http://api.scryfall.com/cards/named?fuzzy={i.replace(" ","+")}'))
    print(i)
    card_request = requests.get(card_request_string)
    card_json = card_request.json()
    set_name = card_json['set']
    card_number = card_json['collector_number']
    rus_card_link = ''.join((f'http://api.scryfall.com/cards/{set_name}/{card_number}/ru'))
    rus_card_request = requests.get(rus_card_link)
    rus_card_json = rus_card_request.json()
    if 'printed_name' in rus_card_json:
        rus_card_name = rus_card_json['printed_name']
    else:
            #card_face = rus_card_json['card_faces']
        rus_card_name = rus_card_json['card_faces'][0]['printed_name'] + ' // ' + rus_card_json['card_faces'][1]['printed_name']
    print(rus_card_name)
    return 0#({'engname':card_json['name'], 'rusname':rus_card_json['card_faces'][0]['printed_name'] + ' // ' + rus_card_json['card_faces'][1]['printed_name']})
print(doubleface('Aberrant Researcher // Perfected Form'))