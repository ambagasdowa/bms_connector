# schemas.py
from typing import Optional, Union

from pydantic import BaseModel


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
    book_id: str
    pages: int
    book_name: str
    is_url: bool
    created: datetime
    modified: datetime
    status: bool


class Config:
    orm_mode = True
