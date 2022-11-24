from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, Numeric, String, Integer, ForeignKey, DateTime, Boolean, Float, Text, MetaData, Table
from sqlalchemy.orm import relationship
from app.base import Base, Engine, Session
import datetime as dt
from flask_login import UserMixin


Base.metadata.create_all(Engine)

#just an exampe of how cards can be, we can house all db related tables in here
class Card(Base):
    __tablename__ = 'cards'
    id = Column(Integer, primary_key = True)
    category_id = Column(Integer, ForeignKey('categories.id'))
    category = relationship("Categories", back_populates='card')
    owner_id = Column(Integer, ForeignKey('users.id'))
<<<<<<< HEAD
    catagory_id = Column(Integer, ForeignKey('catagories.id'))
    card_name = Column(String(100))
    card_description = Column(String(1000))
    def __init__(self, name, description):
        self.card_name = name
        self.card_description = description
=======
    owner = relationship("User", back_populates='card')
    card_name = Column(String(100))
    card_description = Column(String(1000))
    hitpoints = Column(Integer)
    attack = Column(Integer)
    defense = Column(Integer)
    speed = Column(Integer)
    rarity = Column(String(100))
    def __init__(self, name, description, hitpoints, attack, defense, speed, rarity):
        self.card_name = name
        self.card_description = description
        self.hitpoints = hitpoints
        self.attack = attack
        self.defense = defense
        self.speed = speed
        self.rarity = rarity
>>>>>>> schema


class User(Base, UserMixin):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True) # primary keys are required by SQLAlchemy
    card = relationship("Card", back_populates='owner')
    permission_id = Column(Integer, ForeignKey('permissions.id'))
    email = Column(String(100), unique=True)
    password = Column(String(100))
    first_name = Column(String(100))
    last_name = Column(String(100))
    permission_level = Column(Integer, ForeignKey('permission_levels.id'))
    created_at = Column(DateTime)
    def __init__(self, email, password, first_name, last_name, permission_level):
        self.email = email
        self.password = password
        self.first_name = first_name
        self.last_name = last_name
<<<<<<< HEAD
        self.permission_level = permission_level
=======
>>>>>>> schema
        self.created_at = dt.datetime.utcnow()

class Categories(Base):
    __tablename__ = 'categories'
<<<<<<< HEAD
    id = Column(Integer, primary_key=True)
    category_name = Column(String(100))
    category_description = Column(String(1000))
    def __init__(self, name, description):
        self.category_name = name
        self.category_description = description

class Listing(Base):
    __tablename__ = 'listings'
    id = Column(Integer, primary_key=True)
    owner_id = Column(Integer, ForeignKey('cards.id'))
    listing_name = Column(String(100))
    listing_description = Column(String(1000))
    listing_price = Column(Float)
    listing_image = Column(String(1000)) #link to image
    def __init__(self, name, description, price, image):
        self.listing_name = name
        self.listing_description = description
        self.listing_price = price
        self.listing_image = image

class Permissions(Base):
    __tablename__ = 'permission_levels'
    id = Column(Integer, primary_key=True)
    permission_level = Column(String(100))
    def __init__(self, level):
        self.permission_level = level

class Transaction(Base):
    __tablename__ = 'transactions'
    id = Column(Integer, primary_key=True)
    buyer_id = Column(Integer, ForeignKey('users.id'))
    seller_id = Column(Integer, ForeignKey('users.id'))
    listing_id = Column(Integer, ForeignKey('listings.id'))
    transaction_price = Column(Float)
    transaction_date = Column(DateTime)
    def __init__(self, buyer_id, seller_id, listing_id, transaction_price):
        self.buyer_id = buyer_id
        self.seller_id = seller_id
        self.listing_id = listing_id
        self.transaction_price = transaction_price
        self.transaction_date = dt.datetime.utcnow()
=======
    id = Column(Integer, primary_key=True) # primary keys are required by SQLAlchemy
    category = relationship("Card", back_populates='category')
    category_name = Column(String(100))
    def __init__(self, category_name):
        self.category_name = category_name

class Permissions(Base):
    __tablename__ = 'permissions'
    id = Column(Integer, primary_key=True) # primary keys are required by SQLAlchemy
    permission_name = Column(String(50))
    def __init__(self, permission_name):
        self.permission_name = permission_name

class Listing(Base):
    __tablename__ = 'listing'
    id = Column(Integer, primary_key=True) # primary keys are required by SQLAlchemy
    price = Column(Float)
    description = Column(String(1000))
    def __init__(self, price, description):
        self.price = price
        self.description = description

class Transaction(Base):
    __tablename__ = 'transaction'
    id = Column(Integer, primary_key=True) # primary keys are required by SQLAlchemy
    buyer_id = Column(Integer, ForeignKey('users.id'))
    price = Column(Float)
    description = Column(String(1000))
    def __init__(self, price, description):
        self.price = price
        self.description = description
>>>>>>> schema
