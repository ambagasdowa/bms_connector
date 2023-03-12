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
    bms_books_id: int
    bms_bookpages_id: int
    label: str
    created: datetime


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
    bms_books_id: int
    bms_bookpages_id: int
    page: int
    css: str
    created: datetime


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


class SourcePositionsBase(BaseModel):
    bms_books_id: int
    bms_bookpages_id: int
    color: str
    lineWidth: int
    source_width: float
    source_height: float
    default_width: float
    default_height: float
    inputType: str
    page: int
    x1: float
    y1: float
    x2: float
    y2: float
    created: datetime
    modified: Union[datetime, None] = None
    status = bool


class SourcePositionsCreate(BaseModel):
    bms_books_id: int
    bms_bookpages_id: int
    color: str
    lineWidth: int
    source_width: str
    source_height: str
    default_width: str
    default_height: str
    inputType: str
    page: int
    x1: str
    y1: str
    x2: str
    y2: str

    # class Config:
    #     schema_extra = {
    #         "example": [
    #                         {
    #                             "bms_bookpages_id": "6",
    #                             "bms_books_id": "4",
    #                             "color": "cyan",
    #                             "inputType": "radio",
    #                             "lineWidth": "2",
    #                             "page": "3",
    #                             "source_height": "890",
    #                             "source_width": "1440",
    #                             "x1": "120",
    #                             "x2": "230",
    #                             "y1": "80",
    #                             "y2": "40"
    #                         },
    #                         {
    #                             "bms_bookpages_id": "6",
    #                             "bms_books_id": "4",
    #                             "color": "cyan",
    #                             "inputType": "text",
    #                             "lineWidth": "2",
    #                             "page": "3",
    #                             "source_height": "890",
    #                             "source_width": "1440",
    #                             "x1": "120",
    #                             "x2": "230",
    #                             "y1": "80",
    #                             "y2": "40"
    #                         }
    #                     ]
    #     }


class SourcePositionsUpdate(BaseModel):
    pass


class SourcePositions(SourcePositionsBase):
    id: int

    class Config:
        orm_mode = True


# /// Schemes for book pages


# class SourcePageBase(BaseModel):
#     book_pages: Optional[int] = []
#     path: str


# class SourcePageCreate(BaseModel):
#     pass


# class SourcePageUpdate(BaseModel):
#     pass


# class SourcePage(SourcePageBase):
#     id: int
#     book_id: int

#     class Config:
#         orm_mode = True


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
    sourcePositions: Union[list[SourcePositions], None] = None
    # This goes together
    inputs: Union[List[Input]] = []
    inpages: Union[List[Inpage]] = []
    invalues: Union[List[Invalue]] = []

    created: datetime

    def dict(self, **kwargs):
        data = super(ItemBase, self).dict(**kwargs)

        for paper in data['invalues']:
            data['inpages'].append(paper)

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
        # Reorder book_pages and book_pages_maps
        book_pages_maps = {}
        for bookpagesmaps in data['positions']:
            book_pages_maps[bookpagesmaps['page']] = bookpagesmaps['css']

        data['book_pages_maps'] = book_pages_maps

        # Rearrange inputs
        # Change the column name in sql table usr_attr and usr_value
        book_inputs = {}
        ins = {}
        for input_pages in data['inputs']:
            page = input_pages['bms_bookpages_id']
            if book_inputs.get(input_pages['bms_bookpages_id']) is None:
                book_inputs[page] = []
            ins[page] = {}

            for attr in input_pages['data']:
                ins[page][attr['attribute']] = attr['value']
            book_inputs[page].append(ins[page])

        data['book_inputs'] = book_inputs

        del data['inputs']
        del data['inpages']
        del data['positions']
        del data['invalues']
        del data['pagination']

        return data


class ItemCreate(BaseModel):
    book_id: str
    pages: int
    book_name: str
    is_url: bool
    # created: datetime
    created: str
#    status: bool
    # def htmlspecialchars(content):
    #     return content.replace("&", "&amp;").replace('"', "&quot;").replace("'", "&#039;").replace("<", "&lt;").replace(">", "&gt;")


class ItemUpdate(BaseModel):
    book_id: str
    pages: int
    book_name: str
    is_url: bool


class Item(ItemBase):
    id: int

    class Config:
        orm_mode = True


# UPLOAD SECTION

class UploadBase(BaseModel):
    user_id: int
    labelname: str
    file_name: str
    pathname: str
    extname: str
    md5sum: str
    file_size: str
    atime: str
    mtime: str
    ctime: str
    username: str
    datetime_login: str
    ip_remote: str
    created: datetime
    modified: datetime
    status = bool


class UploadCreate(BaseModel):
    file_name: str
    pathname: str

    # class Config:
    #     schema_extra = {
    #         "example": {
    #             "book_name": "Guia de Estudio de Matematicas",
    #         }
    #     }


class UploadUpdate(BaseModel):
    user_id: int
    labelname: str
    file_name: str
    pathname: str
    extname: str
    md5sum: str
    file_size: str
    atime: str
    mtime: str
    ctime: str
    username: str
    datetime_login: str
    ip_remote: str
    created: datetime
    modified: datetime
    status = bool


class Upload(UploadBase):
    id: int

    class Config:
        orm_mode = True


# FILE SECTION

class FileBase(BaseModel):
    book_id: int
    pages: int
    book_name: str
    is_url: bool
    sourcePositions: Union[list[SourcePositions], None] = None
    # urlPages: Union[list[Page], None] = None
    created: datetime
    modified: Union[datetime, None] = None
    status: bool
# TODO: check the reorder in the dataset

    pagination: Union[List[Page], None] = None
    positions: Union[List[Position], None] = None
    # This goes together
    inputs: Union[List[Input], None] = None
    # book_inputs: list[str] = []
#    book_inputs=('test','key',)
    # book_inputs: Union[List[Input]] = []
    # inpages: Union[List[Inpage]] = []
    # invalues: Union[List[Invalue]] = []

    created: datetime

    # def dict(self, **kwargs):
    #     data = super(FileBase, self).dict(**kwargs)

    #     book_pages = {}
    #     for bookpages in data['pagination']:
    #         book_pages[bookpages['book_pages']] = bookpages['path']

    #     data['book_pages'] = book_pages
    #     # Reorder book_pages and book_pages_maps
    #     book_pages_maps = {}
    #     for bookpagesmaps in data['positions']:
    #         book_pages_maps[bookpagesmaps['page']] = bookpagesmaps['css']

    #     data['book_pages_maps'] = book_pages_maps

    #     del data['inputs']
    #     del data['positions']
    #     del data['pagination']
    #     # del data['inpages']
    #     # del data['invalues']

    #     return data


class FileCreate(BaseModel):
    book_id: int
    pages: int
    book_name: str
    is_url: bool
    created: datetime
#    status: bool
#    class Config:
    # schema_extra = {
    #     "example" : {
    #          "book_id": 10,
    #          "pages": 219,
    #          "book_name": "Guia de Estudio de Matematicas",
    #          "is_url": true,
    #          "created": "2022-12-26T23:23:02.071Z",
    #          "modified": "2022-12-26T23:23:02.071Z",
    #          "status": true,
    #    }
    # }


class FileUpdate(BaseModel):
    book_id: int
    pages: int
    book_name: str
    is_url: bool
    modified: datetime
    status: bool


class File(FileBase):
    id: int

    class Config:
        orm_mode = True


# FILE SECTION

class FilelistBase(BaseModel):
    book_id: int
    pages: int
    book_name: str
    is_url: bool
    created: datetime
    modified: Union[datetime, None] = None
    status: bool


class FilelistCreate(BaseModel):
    pass


class FilelistUpdate(BaseModel):
    pass


class Filelist(FileBase):
    id: int

    class Config:
        orm_mode = True
