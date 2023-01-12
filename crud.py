
import pandas as pd
# crud.py
from sqlalchemy.orm import Session
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text,func

from .models import Item, Page,File,Upload,Position,Input,SourcePositions
from .schemas import ItemCreate, ItemUpdate,FileCreate,FileUpdate,UploadCreate,PositionCreate,InputCreate,SourcePositionsCreate
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


def create_item(db: Session, data: ItemCreate):
    db_item = Item(**data.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


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

    # db_item = Item(**data.dict())
    # db.add(db_item)
    # db.commit()
    # db.refresh(db_item)

    # Insert data
    # with Session(bind=engine) as session:

    #     book1 = File(
    #         title="Dead People Who'd Be Influencers Today", str_path=xfile)
    #     book2 = File(title="How To Make Friends In Your 30s")

    #     session.add_all([book1, book2, author1, author2, author3])
    #     session.commit()

    # # Open,close, read file and calculate MD5 on its contents
    #     with open(source, 'rb') as file_to_check:
    #         # read contents of the file
    #         data = file_to_check.read()
    #         # pipe contents of the file through
    #         md5_returned = hashlib.md5(data).hexdigest()

    #     name, ext = os.path.splitext(filename)
    #     # uuid,doctype:FAC,idfac,Date,SomeCtrlnum
    #     split_data = str(name).split('_')

    #     save_file = (split_data[1]+'_'+split_data[2], split_data[0],
    #                  md5_returned, datetime.now().isoformat(timespec='seconds'), '', 1,)

    #     qry_md5 = "select [_md5sum] from sistemas.dbo.cmex_api_controls_files where [_md5sum] = ?"
    #     md5 = False
    #     cursor.execute(qry_md5, (md5_returned,))
    #     for row in cursor.fetchall():
    #         if(row[0] == md5_returned):
    #             md5 = True

    #     if(md5 != True):
    #         print("[blue] save file : "+str(source)+"[blue]")
    #         insert_file = 'insert into sistemas.dbo.cmex_api_controls_files \
    #         (labelname,_filename,_md5sum,created,modified,_status) values( \
    #         ?,?,?,?,?,? \
    #         )'

    #         count = cursor.execute(insert_file, save_file)
    #         cursor.commit()

    #         # get last id from comprobante
    #         cursor.execute(
    #             "select IDENT_CURRENT('sistemas.dbo.cmex_api_controls_files') as id")

    #         cmex_api_controls_files_id = cursor.fetchone()[0]
    #         cursor.commit()
    #         files_ids.append(str(cmex_api_controls_files_id))

    # return {"success": f"Now going to process your files {[file.filename for file in files]}"}
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

# def list_pages(db: Session, skip: int = 0, limit: int = 100):
#     return db.query(Page).offset(skip).limit(limit).all()

def get_srcpos(db: Session, id: int):
    return db.query(SourcePositions).get(id)

def get_srcpos(db: Session, book_id: int, page_id: int):
    return db.query(SourcePositions).filter(SourcePositions.bms_books_id == book_id, SourcePositions.bms_bookpages_id ==page_id).all()

def get_srcpos_ids(db: Session, book_id: int, page_id: int):
    return db.query(SourcePositions).filter(SourcePositions.bms_books_id == book_id, SourcePositions.bms_bookpages_id ==page_id).all()

# def create_srcpos(db: Session,data: SourcePositionsCreate):
#     db_srcpos = SourcePositions(**data.dict())
#     db.add(db_srcpos)
#     db.commit()
#     db.refresh(db_srcpos)
#     return db_srcpos

def create_srcpositions(db: Session, data: SourcePositionsCreate):

    print(f"type ===> {type(data)}")
    print("[green]DATA in crud.py[green]")
    print(data)

#    db_srcpos = SourcePositions(**data.dict())
# NOTE
# Before Save a new input set, first need to remove all remanents in db of 
# that book and that page with:
# db_srcpos.bms_books_id and db_srcpos.bms_bookpages_id
    db_srcpos = SourcePositions(**data.dict())
    db.add(db_srcpos)
    db.commit()
    db.refresh(db_srcpos)
    return db_srcpos



def drop_srcpos(db: Session, srcpos_id: int):
    db.query(SourcePositions).filter(SourcePositions.id == srcpos_id).delete()
    db.commit()
    return None

