from sqlalchemy import Column, String, Integer


from ..db import Base


class Tag(Base):
    __tablename__ = 'Tag'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    Color = Column(String, unique=True)


class Ingredient(Base):
    __tablename__ = 'Ingredient'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    measurement_unit = Column(String)


class Recipe(Base):
    __tablename__ = 'Recipe'

    id = Column(Integer, primary_key=True)
    name = Column(String)
