from sqlalchemy import Column, String, Integer, ForeignKey, Time, Table


from ..db import Base
from ..users.models import User


class Tag(Base):
    __tablename__ = 'tag'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    Color = Column(String, unique=True)


class Ingredient(Base):
    __tablename__ = 'ingredient'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    measurement_unit = Column(String)


class Recipe(Base):
    __tablename__ = 'recipe'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    owner = Column(Integer, ForeignKey(User.id), index=True)
    text = Column(String)
    # TODO: Разобраться с валидацией времени (не менее 1 минуты)
    cooking_time = Column(Time)
    tag = Column(Integer, ForeignKey('tag.id'))
    # TODO: Разобраться как хранить картинки
    image = Column()
    ingredients = Column(Ingredient, ForeignKey('ingredient.id'))


amount_table = Table(
    'amount_table',
    Base.metadata,
    Column('recipe', ForeignKey('recipe.id')),
    Column('ingredient', ForeignKey('ingredient.id')),
    Column('amount', Integer)
)
