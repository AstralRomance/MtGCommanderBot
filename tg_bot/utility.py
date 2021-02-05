def card_scg_link_form(card: str) -> str:
    card = card.replace(' ', '%20')
    return ''.join((STARCITY_LINK,card))

def card_scg_search_form(card: str) -> str:
    card = card.replace(' ', '%20').replace(',',r'%25c%25')
    return ''.join((STARCITY_SEARCH,card))

def get_card_from_scryfall(card_name):
    card_request_string = ''.join((SCRYFALL_API_URL,f'/cards/named?fuzzy={card_name.replace(" ","+")}'))
    card_request = requests.get(card_request_string)
    if card_request.status_code == 404:
        return {'name':0}
    card_json = card_request.json()
    if 'image_uris' in card_json.keys():
        return {'name':card_json['name'], 'image':card_json['image_uris']['normal']}
    else:
        return {'name':card_json['name'], 'image':None}