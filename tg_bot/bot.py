import os
import json
from collections import defaultdict
import requests
from aiogram import Bot, Dispatcher, executor, types
from aiogram.utils.exceptions import BadRequest

SCRYFALL_API_URL = 'https://api.scryfall.com'
STARCITY_SEARCH = r'https://starcitygames.hawksearch.com/sites/starcitygames/?card_name='
STARCITY_LINK = r'https://starcitygames.com/search/?search_query='
bot = Bot(os.environ.get('TG_API_KEY'))
dp = Dispatcher(bot)

def prepare_data(response_cards):
    unacked_dict_list = {k:v for d in response_cards for k, v in d.items()}
    formatted = defaultdict(lambda: {})
    for name, cards in unacked_dict_list.items():
        for suffix in ('Foil',):
            if name.endswith(suffix):
                name = name.replace(suffix, '')
                suffix = 'Foil' if suffix == ' (Foil)' else suffix.strip(' -')
            else:
                suffix = 'C'
            formatted[name][suffix] = cards
    return formatted

def prepare_cards(cards):
    res = [f'\t\t\t\t{state}: {price}' for card in cards for state, price in card.items()]
    return res

def prepare_output(prepared_cards):
    lines = []
    for set_name, variants in prepared_cards.items():
        lines.append(f'<b>{set_name}</b>')
        for variant, cards in sorted(variants.items()):
            if variant != 'C':
                lines.append(f'{variant}: ')
            lines += prepare_cards(cards)
    return lines

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
    if 'image_uris' in cards_json.keys():
        return {'name':card_json['name'], 'image':card_json['image_uris']['normal']}
    else:
        return {'name':card_json['name'], 'image':None}

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

@dp.message_handler()
async def scryfall_find_card(message: types.Message):
    cards_list = message.text.split('\n')
    for card in cards_list:
        card_json = get_card_from_scryfall(card)
        if card_json['name'] == 0:
            return await bot.send_message(message.chat.id, 'Ivalid input or Scryfall troubles')
        card_price = requests.post('http://localhost:9080/crawl.json', data=json.dumps(make_parser_header(card_scg_search_form(card_json['name']))))
        prices = card_price.json()['items']
        
        card_link = card_scg_link_form(card_json['name'])
        response_form = '\n'.join(prepare_output(prepare_data(prices)))
        try:
            if card_json['image'] is not None:
                sender = await bot.send_photo(message.chat.id,
                                    photo=card_json['image'],
                                    caption=f'<a href="{card_link}">{card_json["name"]}</a>\n{response_form}',
                                    parse_mode='HTML')
            else:
                sender = await bot.send_message(message.chat.id,text=f'<a href="{card_link}">{card_json["name"]}</a>\n{response_form}',parse_mode='HTML')
        except BadRequest:
            sender = await bot.send_message(message.chat.id, text=f'<a href="{card_link}">{card_json["name"]}</a>\n{response_form}', parse_mode='HTML')
        return sender

@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    await bot.send_message(message.chat.id, message='Start bot')

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
    
