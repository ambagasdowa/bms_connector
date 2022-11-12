# schemas.py
from typing import List, Optional, Union
from datetime import date, datetime, timedelta

from pydantic import BaseModel

#  `id`                      int unsigned not null auto_increment primary key, -- --> Cual es el pedo?
#  `book_id`                 varchar(255) not null , -- --> ex: 228
#  `pages`                   int null, -- --> 8 total pages
#  `book_name`               varchar(255) null, -- --> Guia_UV
#  `is_url`          bool not null default false, -- --> means false is path url/{book_id} else url?book_id={id}&var=foo
#  `created`                 datetime,
#  `modified`                datetime,
#  `status`                  bool not null default true


# /// Schemes for book pages

class PageBase(BaseModel):
    book_pages: int
    path: str
    css: Optional[str] = []


class PageCreate(BaseModel):
    pass


class PageUpdate(BaseModel):
    pass


class Page(PageBase):
    book_id: str

    class Config:
        orm_mode = True



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


class ItemUpdate(BaseModel):
    book_id: str
    pages: int
    book_name: str
    is_url: bool
    modified: datetime
    status: bool


class Item(ItemBase):
    id: int
    pagination: List[Page] = []

    class Config:
        orm_mode = True



