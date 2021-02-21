import sqlite3 as sql

conn = sql.connect('ScryfallDataBase.db')
cur = conn.cursor()
cur.execute("""CREATE TABLE IF NOT EXISTS cards( 
            english TEXT PRIMARY KEY, 
            russian TEXT, 
            link TEXT);""")
conn.commit()