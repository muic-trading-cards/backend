from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, Numeric, String, Integer, ForeignKey, DateTime, Boolean, Float, Text, MetaData, Table
from sqlalchemy.orm import relationship
from base import Base



#just an exampe of how cards can be, we can house all db related tables in here
class Card(Base):
    __tablename__ = 'card'
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