import os
from db_setup import create_db
from data_collection import get_db, card_search, 

conn = sqlite3.connect('/home/alex/Рабочий стол/DataBase/ScryfallDataBase.db') #connecting to the database
cur = conn.cursor()
link_request = requests.get(link)
link_json = link_request.json()
add_card(link_json['data'])
