# schemas.py
from typing import List, Optional, Union
from datetime import date, datetime, timedelta

from pydantic import BaseModel

# /// Schemes for book inputs-pages values per user


class InvalueBase(BaseModel):
    attribute: str
    value: str


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

        for paper in data['invalues']:
            data['inpages'].append(paper)

#        del data['invalues']

        # data['inputs']['id'] == data['invalues']['bms_inputs_ctrls_id']
        # NOTE rewrite again
        for inpaper in data['inputs']:
            inpaper['data'] = []
            for inval in data['inpages']:
                if (int(inpaper['id']) == int(inval['bms_inputs_ctrls_id'])):
                    inpaper['data'].append(inval)


# Reorder book_pages and book_pages_maps
        book_pages = {}
        for bookpages in data['pagination']:
            book_pages[bookpages['book_pages']] = bookpages['path']

        data['book_pages'] = book_pages
#        del data['pagination']
        # Reorder book_pages and book_pages_maps
        book_pages_maps = {}
        for bookpagesmaps in data['positions']:
            book_pages_maps[bookpagesmaps['page']] = bookpagesmaps['css']

        data['book_pages_maps'] = book_pages_maps
#        del data['positions']

        # Rearrange inputs
        # Change the column name in sql table usr_attr and usr_value
        book_inputs = {}
        ins = {}
        for input_pages in data['inputs']:
#            print(input_pages)
            for attr in input_pages['data']:
                ins[attr['attribute']] = attr['value']

                # try :
                #     ins[attr['attribute']] = attr['value']
                # except :
                #     ins[attr['usr_attr']] = attr['usr_value']

        #         if attr.get('attribute') is None:
        #             ins[attr['usr_attr']] = attr['usr_value']
        #         else:
        #             ins[attr['attribute']] = attr['value']
#            print(ins)
            book_inputs[input_pages['bms_bookpages_id']].append(ins)

        data['book_inputs'] = book_inputs
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
