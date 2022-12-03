from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, Enum, Numeric, String, Integer, ForeignKey, DateTime, Boolean, Float, Text, MetaData, Table
from sqlalchemy.orm import relationship
from app.base import Base, Engine, Session
import datetime as dt
import enum
from flask_login import UserMixin


Base.metadata.create_all(Engine)

#just an exampe of how cards can be, we can house all db related tables in here
class Card(Base):
    __tablename__ = 'cards'
    id = Column(Integer, primary_key = True)
    category_id = Column(Integer, ForeignKey('categories.id'))
    owner_id = Column(Integer, ForeignKey('users.id'))
    listing = relationship("Listing", backref="selling_card", )
    card_name = Column(String(100))
    card_description = Column(String(1000))
    def __init__(self, name, description, owner):
        self.card_name = name
        self.card_description = description
        self.owner = owner


class User(Base, UserMixin):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True) # primary keys are required by SQLAlchemy
    email = Column(String(100), unique=True) 
    password = Column(String(100))
    first_name = Column(String(100))
    last_name = Column(String(100))
    permission_level = Column(Integer, ForeignKey('permission_levels.id'), default=0)
    created_at = Column(DateTime)
    listings = relationship('Listing', backref='owner')
    cards = relationship('Card', backref='owner')
    sellers = relationship('Transaction', backref='seller')
    buyers = relationship('Transaction', backref='buyer')
    def __init__(self, email, password, first_name, last_name):
        self.email = email
        self.password = password
        self.first_name = first_name
        self.last_name = last_name
        self.created_at = dt.datetime.utcnow()

class Categories(Base):
    __tablename__ = 'categories'
    id = Column(Integer, primary_key=True)
    category_name = Column(String(100))
    category_description = Column(String(1000))
    cards = relationship('Card', backref='category')
    def __init__(self, name, description):
        self.category_name = name
        self.category_description = description

class status(enum.Enum):
    sell = 0
    sold = 1

class Listing(Base):
    __tablename__ = 'listings'
    id = Column(Integer, primary_key=True)
    owner_id = Column(Integer, ForeignKey('users.id'))
    card_id = Column(Integer, ForeignKey('cards.id'))
    transaction = relationship("Transaction", backref="transaction_listing", uselist=False)
    listing_name = Column(String(100))
    listing_description = Column(String(1000))
    listing_price = Column(Float)
    listing_image = Column(String(1000)) #link to image
    listing_status = Column(Enum(status), default=status.sell) #status of a listing, 0 = open/selling, 1 = sold
    def __init__(self, name, description, price, image):
        self.listing_name = name
        self.listing_description = description
        self.listing_price = price
        self.listing_image = image

class Permissions(Base):
    __tablename__ = 'permission_levels'
    id = Column(Integer, primary_key=True)
    permission_level = Column(String(100))
    users = relationship('User', backref='permission') #allows user to know their permission
    def __init__(self, level):
        self.permission_level = level

class Transaction(Base):
    __tablename__ = 'transactions'
    id = Column(Integer, primary_key=True)
    buyer_id = Column(Integer, ForeignKey('users.id'))
    listing_id = Column(Integer, ForeignKey('listings.id'))
    transaction_price = Column(Float)
    transaction_date = Column(DateTime)
    def __init__(self, transaction_price):
        self.transaction_price = transaction_price
        self.transaction_date = dt.datetime.utcnow()
