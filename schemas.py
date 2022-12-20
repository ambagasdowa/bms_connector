# schemas.py
from typing import List, Optional, Union
from datetime import date, datetime, timedelta

from pydantic import BaseModel

# /// Schemes for book inputs-pages values per user


class InvalueBase(BaseModel):
    usr_attr: str
    usr_value: str


class InvalueCreate(BaseModel):
    pass


class InvalueUpdate(BaseModel):
    pass


class Invalue(InvalueBase):
    id: int
    bms_inputs_ctrls_id: int
    user_id: int

    class Config:
        orm_mode = True


# /// Schemes for book inputs-pages


class InpageBase(BaseModel):
    attribute: str
    value: str


class InpageCreate(BaseModel):
    pass


class InpageUpdate(BaseModel):
    pass


class Inpage(InpageBase):
    id: int
    bms_inputs_ctrls_id: int

    class Config:
        orm_mode = True

# /// Schemes fot book values and usr values


class InputBase(BaseModel):
    label: str


class InputCreate(BaseModel):
    pass


class InputUpdate(BaseModel):
    pass


class Input(InputBase):
    id: int
    bms_books_id: str
    bms_bookpages_id: str
#    inpages: Optional[Union[List[Inpage]]] = []

    class Config:
        orm_mode = True


# /// Schemes for book positions

class PositionBase(BaseModel):
    page: int
    css: str


class PositionCreate(BaseModel):
    pass


class PositionUpdate(BaseModel):
    pass


class Position(PositionBase):
    id: int

    class Config:
        orm_mode = True

# /// Schemes for book pages


class PageBase(BaseModel):
    book_pages: Optional[int] = []
    path: str
#    basename: Optional[str] = []
#    pathname: Optional[str] = []
#    css: Optional[str] = []


class PageCreate(BaseModel):
    pass


class PageUpdate(BaseModel):
    pass


class Page(PageBase):
    id: int
    bms_books_id: int

    class Config:
        orm_mode = True


class ItemBase(BaseModel):
    book_id: str
    pages: int
    book_name: str
    user_id: int
    is_url: bool
#    modified: datetime
#    status: bool
    pagination: Union[List[Page]] = []
    positions: Union[List[Position]] = []
    # This goes togheter
    inputs: Union[List[Input]] = []
    inpages: Union[List[Inpage]] = []
    invalues: Union[List[Invalue]] = []

    created: datetime

    def dict(self, **kwargs):
        data = super(ItemBase, self).dict(**kwargs)
        xpaper = data['inpages']
        for paper in data['invalues']:
            xpaper.append(paper)

        data['paper'] = xpaper
        return data


class ItemCreate(BaseModel):
    book_id: str
    pages: int
    book_name: str
    is_url: bool
    created: datetime
#    status: bool


class ItemUpdate(BaseModel):
    book_id: str
    pages: int
    book_name: str
    is_url: bool
#    modified: datetime
#    status: bool


class Item(ItemBase):
    id: int

    class Config:
        orm_mode = True
