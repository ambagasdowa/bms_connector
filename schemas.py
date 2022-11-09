# The response model

from typing import Union
from pydantic import BaseModel


class FormsBase(BaseModel):
    attribute : str
    value : str
#    description: Union[str, None] = None

class FormsCreate(FormsBase):
    pass

class Forms(FormsBase):
    user_id : int
    bms_inputs_ctrls_id : int
    bms_books_id : int
    bms_bookpages_id : int

    class Config:
        orm_mode = True


class BooksBase(BaseModel):
    path : str
    css : str


class BooksCreate(BooksBase):
    password : str


class Books(BooksBase):
    book_id : int
    is_url : bool
	book_pages : int
#    items: list[Item] = []

    class Config:
        orm_mode = True
