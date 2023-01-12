# main.py
import uvicorn
from typing import List, Optional, Union
from fastapi import FastAPI, HTTPException, Response, File, Form, UploadFile, Header
import json
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from fastapi.middleware.cors import CORSMiddleware


from fastapi.params import Depends
from sqlalchemy.orm import Session

# UIX
from rich import print
from rich.progress import track
from rich.progress import Progress


# for files
import shutil

from . import models, crud, schemas
from .database import engine, SessionLocal

# Auto creation of database tables
#   If tables already exist, this command does nothing. This allows to
#   safely execute this command at any restart of the application.
#   For a better management of the database schema, it is recommended to
#   integrate specific tools, such as Alembic

# NOTE ru with command:
# uvicorn --reload --host 0.0.0.0 bms_connector.main:app --ssl-keyfile=/var/www/mapache/public_html/src/bms/src/crt_test/server.key --ssl-certfile=/var/www/mapache/public_html/src/bms/src/crt_test/server.crt --ssl-keyfile-password=None


models.Base.metadata.create_all(bind=engine)

# Application bootstrap
#app = FastAPI()
app = FastAPI(
    title='Panamericano API Documentation', docs_url="/api", openapi_url="/api/v1"
)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# This function represents a dependency that can be injected in the endpoints of the API.
# Dependency injection is very smart, as it allows to declaratively require some service.
# This function models the database connection as a service, so that it can be required
# just when needed.
# NOTE https://www.gormanalysis.com/blog/many-to-many-relationships-in-fastapi/
# NOTE https://realpython.com/python-sqlite-sqlalchemy/


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# LIST
# This endpoint returns a list of objects of type `Item` serialized using the `Item` schema that
# we defined in schemas.py. The objects exposed are instances of `models.Item` that are
# validated and serialized as of the definition of the schema `schemas.Item`
@app.get("/items", response_model=List[schemas.Item])
def items_action_list(limit: int = 100, offset: int = 0, db: Session = Depends(get_db)):
    items = crud.list_items(db, offset, limit)
    return items

# RETRIEVE
# This endpoint returns a specific `Item`, given the value of its `id` field,
# which is passed as a path parameter in the URL. It can also return some
# error condition in case the identifier does not correspond to any object


# @app.get("/item/{item_id}", response_model=List[schemas.Item])
# def items_action_retrieve(item_id: str, db: Session = Depends(get_db)):
#    item = crud.get_items(db, item_id)
#    if item is None:
#        raise HTTPException(status_code=404, detail="Book not found")
#    return item

@app.get("/items/{item_id}/{user_id}", response_model=List[schemas.Item])
def items_action_retrieve(item_id: str, user_id: int, db: Session = Depends(get_db)):
    item = crud.get_items(db, item_id, user_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return item

# CREATE
# This endpoint creates a new `Item`. The necessary data is read from the request
# body, which is parsed and validated according to the ItemCreate schema defined beforehand


@app.post("/item/new", response_model=schemas.ItemCreate)
def items_action_create(data: schemas.ItemCreate, db: Session = Depends(get_db)):
    item = crud.create_item(db, data)
    return item

# UPDATE
# This endpoint allows to update an existing `Item`, identified by its primary key passed as a
# path parameter in the url. The necessary data is read from the request
# body, which is parsed and validated according to the ItemUpdate schema defined beforehand


@app.put("/items/{item_id}", response_model=schemas.Item)
def items_action_retrieve(item_id: int, data: schemas.ItemUpdate,  db: Session = Depends(get_db)):
    item = crud.update_item(db, item_id, data)
    if item is None:
        raise HTTPException(status_code=404)
    return item


# DELETE
# This endpoint allows to delete an `Item`, identified by its primary key passed as a
# path parameter in the url. It's worth observing that the status code of the response is
# HTTP 204 No Content, since the response body is empty
@app.delete("/items/{item_id}", status_code=204)
def items_action_retrieve(item_id: int,  db: Session = Depends(get_db)):
    crud.drop_item(db, item_id)
    return None


# //////////////////////////// BMS Pages /////////////////////////////

@app.get("/pages", response_model=List[schemas.Page])
def pages_action_list(limit: int = 100, offset: int = 0, db: Session = Depends(get_db)):
    pages = crud.list_pages(db, offset, limit)
    return pages


@app.get("/page/{page_id}", response_model=schemas.Page)
def pages_action_retrieve(page_id: int, db: Session = Depends(get_db)):
    page = crud.get_page(db, page_id)
    if page is None:
        raise HTTPException(status_code=404, detail="No pages found")
    return page


@app.get("/pages/{book_id}", response_model=List[schemas.Page])
def pages_book_list(book_id: str, db: Session = Depends(get_db)):
    pages = crud.get_pages(db, book_id)
    return pages

# //////////////////////////// Upload zipFiles /////////////////////////////


# @app.post("/file/")
# async def create_file(file: Union[bytes, None] = File(default=None)):
#     if not file:
#         return {"message": "No file sent"}
#     else:
#         return {"file_size": len(file)}


# @app.post("/files/")
# async def create_files(files: List[bytes] = File()):
#     return {"file_sizes": [len(file) for file in files]}


# @app.post("/uploadfile/")
# async def create_upload_file(file: Union[UploadFile, None] = None):
#     if not file:
#         return {"message": "No upload file sent"}
#     else:
#         return {"filename": file.filename}


# @app.post("/uploadfiles/")
# async def create_upload_files(files: List[UploadFile]):
#     if not files:
#         return {"message": "No upload file sent"}
#     else:
#         # call to a function
#         return {"filenames": [file.filename for file in files]}


@app.post("/upload")
async def upload(db: Session = Depends(get_db), book_name: List[Union[str, None]] = None, token: Union[str, None] = Header(default=None, convert_underscores=False), files: List[UploadFile] = File(...)):
    # ask for token and verify
    book_name = book_name[0].split(',')
    proccess = []
    response_book = {}
    if token == 'ioafsyudfoansdfnjnkajsnd017341782yhodklasdhjnallaisdfu==':
        index = 0
        print(f"[red]LIST in book_name : {book_name[0]} at index {str(index)}")
        for file in files:
            try:
                with open(file.filename, 'wb') as f:
                    shutil.copyfileobj(file.file, f)
            except Exception:
                return {"message": f"There was an error uploading the file(s) {file.filename} and token : {token}"}
            else:
                return_id = crud.store_file(book_name[index], db, token, file)
                proccess.append(return_id)
                #proccess.append(crud.store_file(book_name[index], db, token, file))
                response_book[file.filename] = return_id
            finally:
                index = index+1
                file.file.close()

        print("[red] Return JSON : [red]")
        print(response_book)

        return response_book
        #return { "message" : f"Successfuly uploaded {[file.filename for file in files]} and ID {proccess}" }
        #return {"message": f"Successfuly uploaded {[file.filename for file in files]} and {[booking for booking in book_name]}"}
    else:
        return {"message": "your token is invalid"}


# CREATE
# This endpoint creates a new `Item`. The necessary data is read from the request
# body, which is parsed and validated according to the ItemCreate schema defined beforehand

@app.post("/file/add", response_model=schemas.FileCreate)
def files_action_create(data: schemas.FileCreate, db: Session = Depends(get_db)):
    file = crud.create_file(db, data)
    return file

# UPDATE
# This endpoint allows to update an existing `Item`, identified by its primary key passed as a
# path parameter in the url. The necessary data is read from the request
# body, which is parsed and validated according to the ItemUpdate schema defined beforehand


@app.put("/file/{file_id}", response_model=schemas.File)
def files_action_retrieve(file_id: int, data: schemas.FileUpdate,  db: Session = Depends(get_db)):
    file = crud.update_file(db, file_id, data)
    if file is None:
        raise HTTPException(status_code=404)
    return file


#=== === === === === === === === === === === === === === === === === ===
#                       Source Positions
#=== === === === === === === === === === === === === === === === === ===

@app.post("/srcpos/add", response_model=schemas.SourcePositionsCreate)
def srcpos_action_create(data: schemas.SourcePositionsCreate, db: Session = Depends(get_db)):
    sourcePositions = crud.create_srcpos(db, data)
    print(f"[red]SourcePositions : [red][cyan]{sourcePostions}[cyan]")
    return sourcePositions

# UPDATE
# This endpoint allows to update an existing `SourcePositions`, identified by its primary key passed as a
# path parameter in the url. The necessary data is read from the request
# body, which is parsed and validated according to the SourcePositionsUpdate schema defined beforehand


@app.put("/srcpos/{srcpos_id}", response_model=schemas.SourcePositions)
def srcpos_action_retrieve(item_id: int, data: schemas.SourcePositionsUpdate,  db: Session = Depends(get_db)):
    item = crud.update_item(db, item_id, data)
    if item is None:
        raise HTTPException(status_code=404)
    return item


# DELETE
# This endpoint allows to delete an `SourcePositions`, identified by its primary key passed as a
# path parameter in the url. It's worth observing that the status code of the response is
# HTTP 204 No Content, since the response body is empty
@app.delete("/srcpos/{srcpos_id}", status_code=204)
def srcpos_action_retrieve(item_id: int,  db: Session = Depends(get_db)):
    crud.drop_item(db, item_id)
    return None























# if __name__ == "__main__":
#     uvicorn.run(app, host='0.0.0.0',  ssl-keyfile="/var/www/mapache/public_html/src/bms/src/crt_test/server.key", ssl-certfile="/var/www/mapache/public_html/src/bms/src/crt_test/server.crt", ssl-keyfile-password=None)
