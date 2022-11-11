# crud.py
from sqlalchemy.orm import Session

from .models import Item, Page
from .schemas import ItemCreate, ItemUpdate
from typing import Union


def list_books(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Item).offset(skip).limit(limit).all()


def get_book(db: Session, id: int):
    return db.query(Item).get(id)


def create_book(db: Session, data: ItemCreate):
    db_item = Item(**data.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def drop_book(db: Session, item_id: int):
    db.query(Book).filter(Book.id == item_id).delete()
    db.commit()
    return None


def update_book(db: Session, book: Union[int, Book], data: BookUpdate):
    if isinstance(book, int):
        book = get_book(db, book)
    if book is None:
        return None
    for key, value in data:
        setattr(book, key, value)
    db.commit()
    return book

# /// Pages


def list_pages(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Page).offset(skip).limit(limit).all()


def get_page(db: Session, id: int):
    return db.query(Page).get(id)
