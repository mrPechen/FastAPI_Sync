import uuid
from typing import Optional

from pydantic import BaseModel, field_validator


class DishBase(BaseModel):
    title: str
    description: str


class DishCreate(DishBase):
    title: str
    description: str
    price: str


class DishUpdate(DishBase):
    title: str
    description: str
    price: str


class Dish(DishBase):
    id: str
    title: str
    description: str
    price: str

    @field_validator("price")
    def new_price(cls, v):
        return '{:.2f}'.format(float(v.title()))

    class Config:
        from_attributes = True


class SubmenuBase(BaseModel):
    title: str
    description: str


class SubmenuCreate(SubmenuBase):
    title: str
    description: str


class SubmenuUpdate(SubmenuBase):
    title: Optional[str] = None
    description: Optional[str] = None


class Submenu(SubmenuBase):
    id: str
    menu_id: int
    title: str
    description: str
    dishes_count: int

    class Config:
        from_attributes = True


class MenuBase(BaseModel):
    #id: str
    title: str
    description: str


class MenuCreate(MenuBase):
    title: str
    description: str


class MenuUpdate(MenuBase):
    title: Optional[str] = None
    description: Optional[str] = None


class Menu(MenuBase):
    id: str
    title: str
    description: str
    submenus_count: int
    dishes_count: int

    class Config:
        from_attributes = True


class MenuSchema(BaseModel):
    id: int
    name: str
    #submenu_rel: int
    submenu_count: int
    dish_count: int

    class Config:
        from_attributes = True






class SubmenuSchema(SubmenuBase):
    menu_rel: list[MenuBase]






