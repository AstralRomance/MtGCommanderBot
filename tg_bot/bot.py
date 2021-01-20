import os
import json
import requests
from aiogram import Bot, Dispatcher, executor, types

start_urls = []

SCRYFALL_API_URL = 'https://api.scryfall.com'
STARCITY_SEARCH = r'https://starcitygames.hawksearch.com/sites/starcitygames/?card_name='
STARCITY_LINK = r'https://starcitygames.com/search/?search_query='
bot = Bot(os.environ.get('TG_API_KEY'))
dp = Dispatcher(bot)

def card_scg_link_form(card: str) -> str:
    card = card.replace(' ', '%20')
    return ''.join((STARCITY_LINK,card))

def card_scg_search_form(card: str) -> str:
    card = card.replace(' ', '%20').replace(',',r'%25c%25')
    return ''.join((STARCITY_SEARCH,card))

def form_output(card_list: list) -> str:
    outp = ''
    for card_set in card_list:
        for keys in card_set.keys():
            outp += f'{keys}: '
            for cond in card_set[keys]:
                outp += f'{str(*[i for i in cond.items()])}'
        outp += '\n'
    return outp

@dp.message_handler()
async def scryfall_find_card(message: types.Message):
    card_request_string = ''.join((SCRYFALL_API_URL,f'/cards/named?fuzzy={message.text.replace(" ","+")}'))
    card_request = requests.get(card_request_string)
    if (card_request.status_code//100) == 4:
        return await message.reply('Неверное имя карты или проблемы на scryfall')
    
    # if response is not 4**
    response_json = card_request.json()
    card_link = card_scg_link_form(response_json['name'])
    card_search = card_scg_search_form(response_json['name'])

    card_name = response_json['name']
    price_parsing = {
                        'request':
                        {
                            'url':card_search,
                            'dont_filter':True
                        },
                        'spider_name':'starcitygames'
                    }
    card_price = requests.post('http://localhost:9080/crawl.json', data=json.dumps(price_parsing))
    print(card_price.json())
    prices = card_price.json()['items']
    await message.reply_photo(response_json['image_uris']['normal'], caption=f'<a href="{card_link}">{card_name}</a>\n{form_output(prices)}'
                            , parse_mode='HTML')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
    