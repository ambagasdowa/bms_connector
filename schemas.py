# schemas.py
from typing import Optional, Union
from datetime import date, datetime, timedelta

from pydantic import BaseModel


class ItemBase(BaseModel):
    book_id: str
    pages: int
    book_name: str
    is_url: bool
    created: datetime
    modified: datetime
    status: bool


class ItemCreate(BaseModel):
    book_id: str
    pages: int
    book_name: str
    is_url: bool
    created: datetime
    status: bool
#    description: Optional[str] = None


class ItemUpdate(BaseModel):
    book_id: str
    pages: int
    book_name: str
    is_url: bool
    modified: datetime
    status: bool


class Item(ItemBase):
    id: int


class Config:
    orm_mode = True
