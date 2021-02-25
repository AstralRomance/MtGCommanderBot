import os
import sqlite3 as sql

def create_db():
    if os.path.exists('ScryfallDataBase.db'):
        return 'DB already exists'
    else:
        conn = sql.connect('ScryfallDataBase.db')
        cur = conn.cursor()
        cur.execute("""CREATE TABLE IF NOT EXISTS cards( 
                    english TEXT PRIMARY KEY, 
                    russian TEXT, 
                    link TEXT);""")
        conn.commit()
        return 'DB created'
