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


class User(Base, UserMixin):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True) # primary keys are required by SQLAlchemy
    card = relationship("Card", back_populates='owner')
    permission_id = Column(Integer, ForeignKey('permissions.id'))
    email = Column(String(100), unique=True)
    password = Column(String(100))
    first_name = Column(String(100))
    last_name = Column(String(100))
    created_at = Column(DateTime)
    def __init__(self, email, password, first_name, last_name):
        self.email = email
        self.password = password
        self.first_name = first_name
        self.last_name = last_name
        self.created_at = dt.datetime.utcnow()

class Categories(Base):
    __tablename__ = 'categories'
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