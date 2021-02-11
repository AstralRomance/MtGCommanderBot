from sqlalchemy import Table, Column, Integer, String, ForeignKey, MetaData
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.engine.url import URL

DATABASE = {
                'drivername': 'postgres',
                'host': 'localhost',
                'port': '5432',
                'username': 'postgres',
                'password': 'astral100',
                'database': 'mtgCommanderBot'
           }

engine = create_engine(URL(**DATABASE), echo=True)
Base = declarative_base()
class User(Base):
    __tablename__ = 'users'
    tg_id = Column(Integer, primary_key=True)
    tg_username = Column(String)

    def __init__(self, tg_id, tg_username):
        self.tg_id = tg_id
        self.tg_username = tg_username

class Wishlist(Base):
    __tablename__ = 'wishlists'
    id = Column(Integer, primary_key=True)
    card_eng_name = Column(String)
    card_rus_name = Column(String)
    card_price = Column(String)
    owner_id = Column(Integer, ForeignKey('User.tg_id'))
    user = relationship('User', back_populates='wishlist')

    def __init__(self, card_eng_name, card_rus_name, card_price):
        self.card_eng_name = card_eng_name
        self.card_rus_name = card_rus_name
        self.card_price = card_price

class Tradelist(Base):
    __tablename__ = 'tradelists'
    id = Column(Integer, primary_key=True)
    card_eng_name = Column(String)
    card_rus_name = Column(String)
    card_price = Column(String)
    owner_id = Column(Integer, ForeignKey('User.tg_id'))
    user = relationship('User', back_populates='tradelist')

    def __init__(self, card_eng_name, card_rus_name, card_price):
        self.card_eng_name = card_eng_name
        self.card_rus_name = card_rus_name
        self.card_price = card_price


User.wishlists = relationship('Wishlist', back_populates='user')
User.tradelists = relationship('Tradelist', back_populates='user')
Base.metadata.create(engine)
