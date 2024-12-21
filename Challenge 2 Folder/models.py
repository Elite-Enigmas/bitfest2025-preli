from sqlalchemy import Column, Integer, String, Text, Float
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Recipe(Base):
    __tablename__ = "recipes"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    ingredients = Column(Text)
    taste = Column(String)
    cuisine = Column(String)
    preparation_time = Column(Integer)
    instructions = Column(Text)

class IngredientModel(Base):
    __tablename__ = "ingredients"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    quantity = Column(Float)
    unit = Column(String)
