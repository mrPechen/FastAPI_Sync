from sqlalchemy.orm import Session
from . import models, schemas


def get_menus(db: Session):
    return db.query(models.Menu).all()


def get_menu(db: Session, menu_id: int):
    return db.query(models.Menu).filter(models.Menu.id_id == menu_id).first()


def delete_menu(db: Session, menu_id: int):
    delete = db.query(models.Menu).filter(models.Menu.id_id == menu_id).first()
    db.delete(delete)
    db.commit()
    return delete


def update_menu(db: Session, menu_schemas: schemas.MenuUpdate, menu_id: int):
    menu = db.query(models.Menu).filter(models.Menu.id_id == menu_id).first()
    new_data = menu_schemas.dict(exclude_unset=True)
    for key, value in new_data.items():
        setattr(menu, key, value)
    db.add(menu)
    db.commit()
    db.refresh(menu)
    return menu


def create_menu(db: Session, menu: schemas.MenuCreate):
    db_menu = models.Menu(**menu.dict())
    db.add(db_menu)
    db.commit()
    db.refresh(db_menu)
    return db_menu


def get_submenus(db: Session, menu_id: int):
    return db.query(models.Submenu).filter(models.Submenu.menu_id == menu_id).all()


def get_submenu(db: Session, menu_id: int, submenu_id: int):
    return db.query(models.Submenu).filter(models.Submenu.menu_id == menu_id, models.Submenu.id_id == submenu_id).first()


def create_submenu(db: Session, submenu: schemas.SubmenuCreate, menu_id: int):
    db_submenu = models.Submenu(**submenu.dict(), menu_id=menu_id)
    db.add(db_submenu)
    db.commit()
    db.refresh(db_submenu)
    return db_submenu


def update_submenu(db: Session, submenu_schemas: schemas.SubmenuUpdate, menu_id: int, submenu_id: int):
    submenu = db.query(models.Submenu).filter(models.Submenu.menu_id == menu_id, models.Submenu.id_id == submenu_id).first()
    new_data = submenu_schemas.dict(exclude_unset=True)
    for key, value in new_data.items():
        setattr(submenu, key, value)
    db.add(submenu)
    db.commit()
    db.refresh(submenu)
    return submenu


def delete_submenu(db: Session, menu_id: int, submenu_id: int):
    delete = db.query(models.Submenu).filter(models.Submenu.menu_id == menu_id, models.Submenu.id_id == submenu_id).first()
    db.delete(delete)
    db.commit()
    return delete


def get_dishes(db: Session, menu_id: int, submenu_id: int):
    return db.query(models.Dish).filter(models.Dish.menu_id == menu_id, models.Dish.submenu_id == submenu_id).all()


def get_dish(db: Session, menu_id: int, submenu_id: int, dish_id: int):
    return db.query(models.Dish).filter(models.Dish.menu_id == menu_id, models.Dish.submenu_id == submenu_id, models.Dish.id_id == dish_id).first()


def create_dish(db: Session, dish: schemas.DishCreate, menu_id: int, submenu_id: int):
    db_dish = models.Dish(**dish.dict(), menu_id=menu_id, submenu_id=submenu_id)
    db.add(db_dish)
    db.commit()
    db.refresh(db_dish)
    return db_dish


def update_dish(db: Session, dish_schemas: schemas.DishUpdate, menu_id: int, submenu_id: int, dish_id: int):
    dish = db.query(models.Dish).filter(models.Dish.menu_id == menu_id, models.Dish.submenu_id == submenu_id, models.Dish.id_id == dish_id).first()
    new_data = dish_schemas.dict(exclude_unset=True)
    for key, value in new_data.items():
        setattr(dish, key, value)
    db.add(dish)
    db.commit()
    db.refresh(dish)
    return dish


def delete_dish(db: Session, menu_id: int, submenu_id: int, dish_id: int):
    delete = db.query(models.Dish).filter(models.Dish.menu_id == menu_id, models.Dish.submenu_id == submenu_id, models.Dish.id_id == dish_id).first()
    db.delete(delete)
    db.commit()
    return delete
