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
    owner_id = Column(Integer, ForeignKey('users.id'))
    card_name = Column(String(100))
    card_description = Column(String(1000))
    def __init__(self, name, description, hitpoints, attack, defense, speed, rarity):
        self.name = name
        self.description = description
        self.hitpoints = hitpoints
        self.attack = attack
        self.defense = defense
        self.speed = speed
        self.rarity = rarity


class User(Base, UserMixin):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True) # primary keys are required by SQLAlchemy
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