import os
import json
import requests
from aiogram import Bot, Dispatcher, executor, types
from aiogram.utils.exceptions import BadRequest
from utility import card_scg_link_form, card_scg_search_form, get_card_from_scryfall
from output_preparing import prepare_data, prepare_cards, prepare_output, make_parser_header
from URL_CONSTANTS import PARSER_URL


bot = Bot(os.environ.get('TG_API_KEY'))
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    await bot.send_message(message.chat.id, message='Start bot')

@dp.message_handler()
async def scryfall_find_card(message: types.Message):
    cards_list = message.text.split('\n')
    for card in cards_list:
        card_json = get_card_from_scryfall(card)
        if card_json['name'] == 0:
            return await bot.send_message(message.chat.id, 'Ivalid input or Scryfall troubles')
        card_price = requests.post(PARSER_URL, data=json.dumps(make_parser_header(card_scg_search_form(card_json['name']))))
        prices = card_price.json()['items']
        card_link = card_scg_link_form(card_json['name'])
        response_form = '\n'.join(prepare_output(prepare_data(prices)))
        try:
            if card_json['image'] is not None:
                await bot.send_photo(message.chat.id,
                                    photo=card_json['image'],
                                    caption=f'<a href="{card_link}">{card_json["name"]}</a>\n{response_form}',
                                    parse_mode='HTML')
            else:
                await bot.send_message(message.chat.id,text=f'<a href="{card_link}">{card_json["name"]}</a>\n{response_form}',parse_mode='HTML')
        except BadRequest:
            await bot.send_message(message.chat.id, text=f'<a href="{card_link}">{card_json["name"]}</a>\n{response_form}', parse_mode='HTML')

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True) 
