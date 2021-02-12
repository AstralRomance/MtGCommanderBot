from sqlalchemy import Table, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    tg_id = Column(Integer, primary_key=True)

class Wishlist(Base):
    __tablename__ = 'wishlists'
    id = Column(Integer, primary_key=True)
    card_eng_name = Column(String)
    card_rus_name = Column(String)
    card_price = Column(String)
    tg_id = Column(Integer, ForeignKey('users.tg_id'))
    user = relationship('User', back_populates='wishlist')

class Tradelist(Base):
    __tablename__ = 'tradelists'
    id = Column(Integer, primary_key=True)
    card_eng_name = Column(String)
    card_rus_name = Column(String)
    card_price = Column(String)
    tg_id = Column(Integer, ForeignKey('users.tg_id'))
    user = relationship('User', back_populates='tradelist')
