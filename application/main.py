from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from application.db_app import crud, models, schemas
from application.db_app.database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


def connect_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post('/api/v1/menus', response_model=schemas.Menu, status_code=201)
def create_menu(menu: schemas.MenuCreate, db: Session = Depends(connect_db)):
    return crud.create_menu(db=db, menu=menu)


@app.get('/api/v1/menus', response_model=list[schemas.Menu])
def read_menus(db: Session = Depends(connect_db)):
    menu = crud.get_menus(db=db)
    return menu


@app.patch('/api/v1/menus/{target_menu_id}', response_model=schemas.Menu)
def update_menus(target_menu_id: int, menu: schemas.MenuUpdate, db: Session = Depends(connect_db)):
    check_menu = crud.get_menu(db=db, menu_id=target_menu_id)
    if not check_menu:
        return HTTPException(status_code=404, detail='menu not found')
    return crud.update_menu(db=db, menu_schemas=menu, menu_id=target_menu_id)


@app.delete('/api/v1/menus/{target_menu_id}')
def delete_menus(target_menu_id: int, db: Session = Depends(connect_db)):
    check_menu = crud.get_menu(db=db, menu_id=target_menu_id)
    if not check_menu:
        return HTTPException(status_code=404, detail='menu not found')
    crud.delete_menu(db=db, menu_id=target_menu_id)
    return {"status": True, "message": "The menu has been deleted"}


@app.get('/api/v1/menus/{target_menu_id}', response_model=schemas.Menu)
def read_menu(target_menu_id: int, db: Session = Depends(connect_db)):
    menu = crud.get_menu(db=db, menu_id=target_menu_id)
    if not menu:
        raise HTTPException(status_code=404, detail='menu not found')
    return menu


@app.post('/api/v1/menus/{target_menu_id}/submenus', response_model=schemas.Submenu, status_code=201)
def create_submenu(target_menu_id: int, submenu: schemas.SubmenuCreate, db: Session = Depends(connect_db)):
    check_menu = crud.get_menu(db=db, menu_id=target_menu_id)
    if not check_menu:
        raise HTTPException(status_code=404, detail='menu not found')
    return crud.create_submenu(db=db, submenu=submenu, menu_id=target_menu_id)


@app.get('/api/v1/menus/{target_menu_id}/submenus', response_model=list[schemas.Submenu])
def read_submenus(target_menu_id: int, db: Session = Depends(connect_db)):
    submenu = crud.get_submenus(db=db, menu_id=target_menu_id)
    return submenu


@app.patch('/api/v1/menus/{target_menu_id}/submenus/{target_submenu_id}', response_model=schemas.Submenu)
def update_submenu(target_menu_id: int, target_submenu_id: int, submenu: schemas.SubmenuUpdate, db: Session = Depends(connect_db)):
    check_submenu = crud.get_submenu(db=db, menu_id=target_menu_id, submenu_id=target_submenu_id)
    if not check_submenu:
        return HTTPException(status_code=404, detail='menu id or submenu id not found')
    return crud.update_submenu(db=db, submenu_schemas=submenu, menu_id=target_menu_id, submenu_id=target_submenu_id)


@app.delete('/api/v1/menus/{target_menu_id}/submenus/{target_submenu_id}')
def delete_submenus(target_menu_id: int, target_submenu_id: int, db: Session = Depends(connect_db)):
    check_submenu = crud.get_submenu(db=db, menu_id=target_menu_id, submenu_id=target_submenu_id)
    if not check_submenu:
        return HTTPException(status_code=404, detail='menu id or submenu id not found')
    crud.delete_submenu(db=db, menu_id=target_menu_id, submenu_id=target_submenu_id)
    return {"status": True, "message": "The submenu has been deleted"}


@app.get('/api/v1/menus/{target_menu_id}/submenus/{target_submenu_id}', response_model=schemas.Submenu)
def read_submenu(target_menu_id: int, target_submenu_id: int, db: Session = Depends(connect_db)):
    submenu = crud.get_submenu(db=db, menu_id=target_menu_id, submenu_id=target_submenu_id)
    if not submenu:
        raise HTTPException(status_code=404, detail='submenu not found')
    return submenu


@app.post('/api/v1/menus/{target_menu_id}/submenus/{target_submenu_id}/dishes', response_model=schemas.Dish, status_code=201)
def create_dish(target_menu_id: int, target_submenu_id: int, dish: schemas.DishCreate, db: Session = Depends(connect_db)):
    check_submenu = crud.get_submenu(db=db, menu_id=target_menu_id, submenu_id=target_submenu_id)
    if not check_submenu:
        return HTTPException(status_code=404, detail='menu id or submenu id not found')
    create = crud.create_dish(db=db, dish=dish, menu_id=target_menu_id, submenu_id=target_submenu_id)
    return create


@app.get('/api/v1/menus/{target_menu_id}/submenus/{target_submenu_id}/dishes', response_model=list[schemas.Dish])
def read_dishes(target_menu_id: int, target_submenu_id: int, db: Session = Depends(connect_db)):
    result = crud.get_dishes(db=db, menu_id=target_menu_id, submenu_id=target_submenu_id)
    return result


@app.patch('/api/v1/menus/{target_menu_id}/submenus/{target_submenu_id}/dishes/{target_dish_id}', response_model=schemas.Dish)
def update_dish(target_menu_id: int, target_submenu_id: int, target_dish_id: int, dish: schemas.DishUpdate, db: Session = Depends(connect_db)):
    dish = crud.update_dish(db=db, dish_schemas=dish, menu_id=target_menu_id, submenu_id=target_submenu_id, dish_id=target_dish_id)
    if not dish:
        return HTTPException(status_code=404, detail='menu id, submenu id or dish id not found')
    return dish


@app.delete('/api/v1/menus/{target_menu_id}/submenus/{target_submenu_id}/dishes/{target_dish_id}')
def delete_dish(target_menu_id: int, target_submenu_id: int, target_dish_id: int, db: Session = Depends(connect_db)):
    check_dish = crud.get_dish(db=db, menu_id=target_menu_id, submenu_id=target_submenu_id, dish_id=target_dish_id)
    if not check_dish:
        raise HTTPException(status_code=404, detail='menu id, submenu id or dish id not found')
    crud.delete_dish(db=db, menu_id=target_menu_id, submenu_id=target_submenu_id, dish_id=target_dish_id)
    return {"status": True, "message": "The dish has been deleted"}


@app.get('/api/v1/menus/{target_menu_id}/submenus/{target_submenu_id}/dishes/{target_dish_id}', response_model=schemas.Dish)
def read_dish(target_menu_id: int, target_submenu_id: int, target_dish_id: int, db: Session = Depends(connect_db)):
    result = crud.get_dish(db=db, menu_id=target_menu_id, submenu_id=target_submenu_id, dish_id=target_dish_id)
    if not result:
        raise HTTPException(status_code=404, detail='dish not found')
    return result
