from sqlalchemy import Column, ForeignKey, Integer, String, Float, func
from sqlalchemy.ext import compiler
from sqlalchemy.ext.hybrid import hybrid_property, cast
from sqlalchemy.orm import relationship, column_property
from .database import Base
import uuid


class Menu(Base):
    __tablename__ = 'menu'

    id_id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    submenu_rel = relationship('Submenu', cascade='all,delete', back_populates='menu_rel')
    dish_rel = relationship('Dish', cascade='all,delete', back_populates='menu_rel2')

    @hybrid_property
    def submenus_count(self):
        return len(self.submenu_rel)

    @hybrid_property
    def dishes_count(self):
        return len(self.dish_rel)

    @hybrid_property
    def id(self):
        return str(self.id_id)



class Submenu(Base):
    __tablename__ = 'submenu'

    id_id = Column(Integer, primary_key=True, index=True)
    title = Column(String, unique=True)
    description = Column(String)
    menu_id = Column(Integer, ForeignKey('menu.id_id'))
    menu_rel = relationship('Menu', back_populates='submenu_rel')
    dish = relationship('Dish', cascade='all, delete', back_populates='submenu_rel')

    @hybrid_property
    def dishes_count(self):
        return len(self.dish)

    @hybrid_property
    def id(self):
        return str(self.id_id)


class Dish(Base):
    __tablename__ = 'dishes'

    id_id = Column(Integer, primary_key=True, index=True)
    title = Column(String, unique=True)
    description = Column(String)
    price = Column(String)
    submenu_id = Column(Integer, ForeignKey('submenu.id_id'))
    submenu_rel = relationship('Submenu', back_populates='dish')
    menu_rel2 = relationship('Menu', back_populates='dish_rel')
    menu_id = Column(Integer, ForeignKey('menu.id_id'))

    @hybrid_property
    def id(self):
        return str(self.id_id)




