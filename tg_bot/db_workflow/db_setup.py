from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL

from models import User, Wishlist, Tradelist, Base

DATABASE = {
                'drivername': 'postgres',
                'host': 'localhost',
                'port': '5432',
                'username': 'mtgCommanderBot',
                'password': 'astral100',
                'database': 'mtgCommanderBot'
           }

engine = create_engine(URL(**DATABASE), echo=True)
Base.metadata.create_all(engine)
