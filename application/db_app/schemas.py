from typing import Optional
from pydantic import BaseModel, field_validator, ConfigDict


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
    model_config = ConfigDict(from_attributes=True)

    @field_validator("price")
    def new_price(cls, v):
        return '{:.2f}'.format(float(v.title()))


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
    model_config = ConfigDict(from_attributes=True)


class MenuBase(BaseModel):
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
    model_config = ConfigDict(from_attributes=True)


