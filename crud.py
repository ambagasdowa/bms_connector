
import pandas as pd
# crud.py
from sqlalchemy.orm import Session
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text,func

from fastapi import FastAPI
from pydantic import BaseModel

from fastapi import Response
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder


from .models import Item, Page,File,Filelist,Upload,Position,Input,Inpage,Invalue,SourcePositions,Invalue
from .schemas import ItemUpdate,FileCreate,FileUpdate,UploadCreate,PositionCreate,InputCreate,SourcePositionsCreate
from typing import Union,List

import urllib
import os
from os.path import join, splitext
import glob
import sys
import subprocess
from datetime import datetime, date, tzinfo, timedelta
import time
from re import split, sub
# Zip
import zipfile
# md5
import hashlib

from collections import Counter
# UIX
from rich import print
from rich.progress import track
from rich.progress import Progress


from .config import configuration

config = configuration['download_config']

# NOTE search for books with data 

def list_items(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Item).offset(skip).limit(limit).all()


def get_items(db: Session, book_id: str, user_id: int):
    return db.query(Item).filter(Item.book_id == book_id, Item.user_id == user_id).all()
#    return Response(content=db.query(Item).filter(Item.book_id == book_id, Item.user_id == user_id).all(), media_type="application/json")


def get_item(db: Session, id: int):
    return db.query(Item).get(id)


# def create_item(db: Session, data: ItemCreate):
#     db_item = Item(**data.dict())
#     db.add(db_item)
#     db.commit()
#     db.refresh(db_item)
#     return db_item


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


def get_pages(db: Session, book_id: str):
    return db.query(Page).filter(Page.book_id == book_id).all()

# One with have the files


def get_files(path):
    for file in os.listdir(path):
        if os.path.isfile(os.path.join(path, file)):
            yield file


def store_file( book_name:str ,db:Session,  token:str, file):
    """TODO: Docstring for store_file.

    :arg1: TODO
    :returns: TODO
    https --verify=no -f POST 10.14.17.105:8000/upload files@~/Development/book_matematicas_002_bachillerato_20221223.zip files@~/Development/guia_unam_215_universidad_20221223.zip files@~/Development/guia_uv_002_demo_20221223.zip
    """
    print(f"[red]token : {token}[red]")
    print(f"[cyan]FILE {type(file)}[cyan]")

    filename = file.filename
    tmp_path = config['download_path'] + config['dir_path']
    date_up = datetime.now()
#    clean_dir_files = subprocess.run(["rm", "-r", tmp_path], stdout=subprocess.DEVNULL)
# book_matematicas_002_bachillerato_20221223.zip
    spl = str(filename.replace('.zip', ''))
#    if not set the book_name take it from zip-filename

    # if book_name : 
    #     print(f"TYPE of Book : {type(book_name)}")
    #     print(f"{book_name}")

    if not book_name :
        book_name = spl.replace('_',' ').capitalize()

    spl_path = str(spl.replace('_','/'))

    dir_path = '/' + spl_path
    print("NEW PATH : " + dir_path)

    store_path = config['basename']+config['pathname']+dir_path
    make_dir_files = subprocess.run(
        ["mkdir", "-p", tmp_path+"pack", tmp_path+"unpack", store_path], stdout=subprocess.DEVNULL)

#    for file in files :
    print(file)
    print(f"THE FILENAME :  {filename}")

    download_path = config['download_path']
#    dir_path = config['dir_path']

    pack = download_path+dir_path+"pack/"
    unpack = download_path+dir_path+"unpack/"

    try:
        with zipfile.ZipFile(filename, 'r') as zip_ref:
            zip_ref.extractall(store_path)
    except zipfile.BadZipfile:
        print("[red] zip file : " + filename +
              " from provider with errors , try again ...[red]")

    # Create Book
#    with Session(bind=engine) as session:
    book = Upload(
        file_name = filename
        ,pathname = store_path
    )
    db.add(book)
    db.commit()
    db.refresh(book)

    print(f"[blue]The book ID : {book.id}[blue]")



    full_path = store_path+'/'+'pages'
    cnt_ext = Counter()
    ext_dict = {}
    x = []
    for xfile in get_files(full_path):
        x.append(splitext(xfile)[1])

    for z in x:
        cnt_ext[z] += 1

    print(f"[red]count :{cnt_ext}[red]")
    extension = max(cnt_ext)
    print(f"EXTENSION : [red] {extension} [red]")
    pages_count = len(glob.glob1(full_path,f"*{extension}"))
    print(f"[gray]pages : [green]{pages_count}[green]")

#    Create the book
    book_file = File(
        book_id = book.id
        ,pages = pages_count
        ,book_name = book_name
        ,is_url = True
        ,created = date_up
    )
    db.add(book_file)
    db.commit()
    db.refresh(book_file)

    print(f"[cyan]The book_file ID[cyan] : [blue]{book_file.id}[blue]")

    for i in range(int(pages_count)):
    #    Add pages
    #    save each page with a counter
        current_page = i + 1
        book_pages = Page(
        bms_books_id     = book.id
        ,book_pages      = current_page
        ,basename        = config['ext_basename']+config['pathname']
        ,pathname        = dir_path +'/pages/'+ str(current_page) + extension
        ,created         = date_up
        )
        db.add(book_pages)
        db.commit()
        db.refresh(book_pages)
        print(f"[cyan]The book_file ID[cyan] : [blue]{book_pages.id}[blue]")
# Set entries in positions
        book_positions = Position(
            bms_books_id = book.id
            ,bms_bookpages_id = book_pages.id
            ,page = current_page
            ,css = ''
            ,created = date_up
        )
        db.add(book_positions)
        db.commit()
        db.refresh(book_positions)

        print(f"[cyan]The book_positions ID[cyan] : [blue]{book_positions.id}[blue]")

# Set entries in inputs container
        book_input = Input(
            bms_books_id = book.id
            ,bms_bookpages_id = current_page
            ,label = f"Input entry for book {book.id} in pages {current_page}"
            ,created = date_up
        )
        db.add(book_input)
        db.commit()
        db.refresh(book_input)

        print(f"[cyan]The book_input ID[cyan] : [blue]{book_input.id}[blue]")

    #db.execute(func.bms_proc_build_cache_inp_usr())
    query = '{0} {1}.{2}'.format( configuration['db_connection']['proc_exec'],configuration['db_connection']['database'] ,configuration['db_connection']['proc_0'])
    db.execute(query)
    db.commit()

    return book.id



def create_file(db: Session, data: FileCreate):

    db_file = File(**data.dict())
    db.add(db_file)
    db.commit()
    db.refresh(db_file)
    return db_file

def update_file(db: Session, file: Union[int, File], data: FileUpdate):

    if isinstance(file, int):
        file = get_file(db, file)
    if file is None:
        return None
    for key, value in data:
        setattr(file, key, value)
    db.commit()
    return file


#=== === === === === === === === === === === === === === === === === === 
#                      Source Positions
#=== === === === === === === === === === === === === === === === === === 


def get_srcpos(db: Session, book_id: int, page_id: int):
    return db.query(SourcePositions).filter(SourcePositions.bms_books_id == book_id, SourcePositions.bms_bookpages_id ==page_id).all()

def get_srcpos_ids(db: Session, book_id: int, page_id: int):
    return db.query(SourcePositions).filter(SourcePositions.bms_books_id == book_id, SourcePositions.bms_bookpages_id ==page_id).all()

def get_srcpositions(db: Session, book_id: int):
    # request = get params book_id,user_id,etc
    #   if request with urls , inputs , positions . default layout
    # return request

    return db.query(File).filter(File.book_id == book_id).all()


def create_srcpositions(db: Session, data: SourcePositionsCreate):

    print(f"type ===> {type(data)}")
    print("[green]DATA in crud.py[green]")
    print(data)
# NOTE
# Before Save a new input set, first need to remove all remanents in db of 
# that book and that page with:
# db_srcpos.bms_books_id and db_srcpos.bms_bookpages_id
    db_srcpos = SourcePositions(**data.dict())
# NOTE check first the data from db_srcpos and set to bms_positions and bms_inputs_ctrls and bms_inputs_pages from bms_src_positions
    # bms_inputs_ctrls
    # bms_inputs_pages
    # bms_inputs_values
    # bms_positions {keys:{}}
    # bms_src_positions
    print(db_srcpos)
    #first set an entry in bms_inputs_ctrls
    bid = db_srcpos.bms_books_id
    bp = db_srcpos.page
    # Set an entry in bms_inputs_pages
    itype = db_srcpos.inputType
    createdTime = datetime.now()
    print(bid,bp,itype)


# Set entries in inputs container
    bk_input = Input(
         bms_books_id = bid
        ,bms_bookpages_id = bp
        ,label = f"Input entry for book {bid} in page => {bp}"
        ,created = createdTime
    )
    db.add(bk_input)
    db.commit()
    db.refresh(bk_input)

    print(f"[cyan]The bk_input linked with POSITIONS ID[/cyan] : [blue]{bk_input.id}[/blue]")

    
    datav = {"type":itype,"name":f"inp{bk_input.id}","id":f"inp{bk_input.id}","autofocus":"on"}

    for attr,data in datav.items():
        bk_inpages = Inpage(
             bms_inputs_ctrls_id=bk_inputs.id
            ,attribute = attr
            ,value = data
            ,created = createdTime
        )
        db.add(bk_inpages)
        db.commit()
        db.refresh(bk_inpages)

#WORKING FROM HIR
# Set entries in bms_inputs_pages
    # input_pages = Invalue(
    #      bms_books_id = bid
    #     ,bms_bookpages_id = bp
    #     ,label = f"Input entry for book {book.id} in pages {current_page}"
    #     ,created = datetime.now()
    # )
    # db.add(input_pages)
    # db.commit()
    # db.refresh(input_pages)

    # print(f"[cyan]The book_input ID[cyan] : [blue]{book_input.id}[blue]")

    db.add(db_srcpos)
    db.commit()
    db.refresh(db_srcpos)
    return db_srcpos



def drop_srcpositions(db: Session, book_id: int,page_id:int):
    db.query(SourcePositions).filter(SourcePositions.bms_books_id == book_id,SourcePositions.bms_bookpages_id == page_id).delete()
    #drop attributes values too ? or update ids
    # search each id in db and update id relations 
    db.commit()
    return {"ok":True}


def list_books(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Filelist).offset(skip).limit(limit).all()

def get_book(db: Session, book_id: str, user_id: int):
    # return get_book_usr(db,book_id,user_id)
    return db.query(Item).filter(Item.book_id == book_id, Item.user_id == user_id).all()


#def get_book_usr(db:Session,book_id:int,user_id:int):
#    print(f"[red]book_id ->[blue] {book_id}")
#    print(f"[red]user_id ->[blue] {user_id}")

#    #have book_id 
#    #MariaDB root@127.0.0.1:db_ediq2021> describe bms_inputs_ctrls
#    # ================  ================  ====  ===  =======  ==============
#    # Field             Type              Null  Key  Default  Extra
#    # ================  ================  ====  ===  =======  ==============
#    # id                int(10) unsigned  NO    PRI  <null>   auto_increment
#    # bms_books_id      int(10) unsigned  NO         <null>
#    # bms_bookpages_id  int(10) unsigned  NO         <null>
#    # label             text              YES        <null>
#    # created           datetime          YES        <null>
#    # modified          datetime          YES        <null>
#    # status            tinyint(1)        NO         1
#    # ================  ================  ====  ===  =======  ==============

#    # select * from bms_inputs_ctrls where bms_books_id = book_id
#    # return id,bms_book_id,bms_bookpages_id
#    # MariaDB root@127.0.0.1:db_ediq2021> describe bms_inputs_values
#    # ===================  ================  ====  ===  =======  ==============
#    # Field                Type              Null  Key  Default  Extra
#    # ===================  ================  ====  ===  =======  ==============
#    # id                   int(10) unsigned  NO    PRI  <null>   auto_increment
#    # bms_inputs_ctrls_id  int(10) unsigned  NO         <null>
#    # user_id              int(10) unsigned  NO --> not in bms_inputs_pages
#    # attribute            varchar(255)      YES        <null>
#    # value                text              YES        <null>
#    # created              datetime          YES        <null>
#    # modified             datetime          YES        <null>
#    # status               tinyint(1)        NO         1
#    # ===================  ================  ====  ===  =======  ==============
#    # make the arrange



#    #inputs_ctrls = db.query(Input).filter(Input.bms_books_id == book_id).all()

#    #book_input = {}
#    #book_inputs = []
#    #inner_input = []
#    #inner_block = {}
#    #books = []
#    #input_pages = []
#    #new_response = {}

#    #for b in inputs_ctrls:
#    #    print(f"[red]{b.id},{b.bms_books_id},{b.bms_bookpages_id},{b.label}[/red]")
#    #    book_input[b.bms_bookpages_id] = {}
#    #    inputs_pages = db.query(Inpage).filter(Inpage.bms_inputs_ctrls_id == b.id).all()

#    #    for k in inputs_pages:
#    #        print(jsonable_encoder(k))
#    #        print(f"[green]{k.id},{k.bms_inputs_ctrls_id},{k.attribute},{k.value}[/green]")


#    #        kid = b.bms_books_id
#    #        inblock = jsonable_encoder(k)
#    #        inner_input.append(inblock)

#    #        inner_block= inner_block, f"{kid}:{inblock}"


#    #        if book_input[b.bms_bookpages_id] is None:
#    #            book_input[b.bms_bookpages_id] = []

#    #        #book_input[b.bms_bookpages_id][k.attribute] = k.value
#    #        # book_input[b.bms_bookpages_id].append(inblock,)

#    #        # books.append((b.bms_bookpages_id,k.id,k.attribute,k.value),)

#    #    inputs_values = db.query(Invalue).filter(Invalue.bms_inputs_ctrls_id == b.id,Invalue.user_id == user_id).all()
#    #    for x in inputs_values:
#    #        print(f"[cyan]{x.id},{x.bms_inputs_ctrls_id},{x.attribute},{x.value},{x.user_id}[/cyan]")

###            book_input[b.bms_bookpages_id][x.attribute] = x.value
#    #        book_input[b.bms_bookpages_id] = (jsonable_encoder(x),)
#    #        books.append((b.bms_bookpages_id,x.id,x.attribute,x.value,))



#    ## book_inputs.append(book_input)
#    #print(inner_input)
#    #print(inner_block)
#    #print(jsonable_encoder(book_input))

#    response = db.query(File).filter(File.book_id == book_id).all()
#    # setattr(response[0], 'book_inputs', jsonable_encoder(book_inputs))

#    # for resp in response:
#    #     print(resp.sourcePositions)
#    #     print(resp.inputs)
#    #     print(resp.positions)
#    #     print(resp.pagination)

#    # new_response = jsonable_encoder(response)
#    # print("[red]JASONABLE:")
#    # print(type(new_response))
#    # print(new_response)
#    # new_response['book_inputs'] = jsonable_encoder(book_inputs)

#    # for data in response:
#    #     print(type(data))
#    #     # response_json = jsonable_encoder(data)
#    #     # response_json['book_inputs'] = book_inputs
#    #     # setattr(data,'book_inputs',book_inputs)
#    #     # print(JSONResponse(content=jsonable_encoder(data)))
#    #     print(jsonable_encoder(data))

#    # return book_inputs

#    if len(response) == 0 :
#        print(f"[red]book id[/red] [cyan] {book_id}[/cyan][red] not found")
#        return None
#    else:
#        print(f"length of list -> {len(response)}")
#        #return JSONResponse(content=jsonable_encoder(response))
#        return response

