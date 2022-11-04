from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, Numeric, String, Integer, ForeignKey, DateTime, Boolean, Float, Text, MetaData, Table
from sqlalchemy.orm import relationship
from app.base import Base, Engine, Session
import datetime as dt


Base.metadata.create_all(Engine)

#just an exampe of how cards can be, we can house all db related tables in here
class Card(Base):
    __tablename__ = 'cards'
    id = Column(Integer, primary_key = True)
    name = Column(String(100), nullable = False)
    description = Column(String(1000), nullable = False)
    hitpoints = Column(Integer, nullable = False)
    attack = Column(Integer, nullable = False)
    defense = Column(Integer, nullable = False)
    speed = Column(Integer, nullable = False)
    rarity = Column(String(100), nullable = False)
    def __init__(self, name, description, hitpoints, attack, defense, speed, rarity):
        self.name = name
        self.description = description
        self.hitpoints = hitpoints
        self.attack = attack
        self.defense = defense
        self.speed = speed
        self.rarity = rarity


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True) # primary keys are required by SQLAlchemy
    card_id = Column(Integer, ForeignKey('cards.id'))
    email = Column(String(100), unique=True)
    password = Column(String(100))
    name = Column(String(1000))
    created_at = Column(DateTime)
    def __init__(self, email, password, name):
        self.email = email
        self.password = password
        self.name = name
        self.created_at = dt.datetime.utcnow()