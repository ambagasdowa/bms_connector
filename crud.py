# crud.py
from sqlalchemy.orm import Session

from .models import Item, Page
from .schemas import ItemCreate, ItemUpdate
from typing import Union


def list_items(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Item).offset(skip).limit(limit).all()

def get_items(db: Session, book_id:str,user_id:int):
    return db.query(Item).filter(Item.book_id == book_id,Item.user_id==user_id).all()

def get_item(db: Session, id: int):
    return db.query(Item).get(id)


def create_item(db: Session, data: ItemCreate):
    db_item = Item(**data.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def drop_item(db: Session, item_id: int):
    db.query(Item).filter(Item.id == item_id).delete()
    db.commit()
    return None


def update_item(db: Session, item: Union[int, Item], data: ItemUpdate):
    if isinstance(item, int):
        item = get_item(db, item)
    if item is None:
        return None
    for key, value in data:
        setattr(item, key, value)
    db.commit()
    return item

# /// Pages


def list_pages(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Page).offset(skip).limit(limit).all()

def get_page(db: Session, id: int):
    return db.query(Page).get(id)

def get_pages(db: Session, book_id:str):
    return db.query(Page).filter(Page.book_id == book_id).all()



