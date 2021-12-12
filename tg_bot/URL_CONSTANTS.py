import os

SCRYFALL_API_URL = 'https://api.scryfall.com'
STARCITY_SEARCH = r'https://starcitygames.hawksearch.com/sites/starcitygames/?card_name='
STARCITY_LINK = r'https://starcitygames.com/search/?search_query='
PARSER_URL = f'http://{os.environ.get("SCRAPY_CONTAINER")}:{os.environ.get("SCRAPY_PORT")}/crawl.json'
