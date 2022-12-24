# crud.py
from sqlalchemy.orm import Session
from sqlalchemy.orm import sessionmaker

from .models import Item, Page
from .schemas import ItemCreate, ItemUpdate
from typing import Union

import urllib
import os
import sys
import subprocess
from datetime import datetime, date, tzinfo, timedelta
import time
from re import split, sub
# Zip
import zipfile
# md5
import hashlib

from .config import configuration

config = configuration['download_config']


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


def store_file(file, token):
    """TODO: Docstring for store_file.

    :arg1: TODO
    :returns: TODO
    https --verify=no -f POST 10.14.17.105:8000/upload files@~/Development/book_matematicas_002_bachillerato_20221223.zip files@~/Development/guia_unam_215_universidad_20221223.zip files@~/Development/guia_uv_002_demo_20221223.zip
    """
    print(f"token : {token}")
    filename = file.filename
    tmp_path = config['download_path'] + config['dir_path']
#    clean_dir_files = subprocess.run(["rm", "-r", tmp_path], stdout=subprocess.DEVNULL)
# book_matematicas_002_bachillerato_20221223.zip
    spl = str(filename.replace('.zip', '')).split('_')

    type_book = spl[0]
    type_course = spl[1]
    type_serial = spl[2]
    type_degree = spl[3]
   # type_date = spl[4]

    dir_path = '/'+type_book+'/'+type_course+'/'+type_serial+'/'+type_degree
    #dir_path = (split_data[0]+'/'+split_data[1], split_data[0],md5_returned, datetime.now().isoformat(timespec='seconds'), '', 1,)

    store_path = config['basename']+config['pathname']+dir_path
    make_dir_files = subprocess.run(
        ["mkdir", "-p", tmp_path+"pack", tmp_path+"unpack", store_path], stdout=subprocess.DEVNULL)

#    for file in files :
    print(file)
    print(f"THE FILENAME :  {filename}")

    download_path = config['download_path']
    dir_path = config['dir_path']

    pack = download_path+dir_path+"pack/"
    unpack = download_path+dir_path+"unpack/"

    try:
        with zipfile.ZipFile(filename, 'r') as zip_ref:
            zip_ref.extractall(store_path)
    except zipfile.BadZipfile:
        print("[red] zip file : " + filename +
              " from provider with errors , try again ...[red]")

    xfiles = []
    for xfile in get_files(store_path+'/'+'/pages'):
        xfiles.append(xfile)

    print(xfiles)

    # Insert data
    # with Session(bind=engine) as session:

    #     book1 = Book(title="Dead People Who'd Be Influencers Today")
    #     book2 = Book(title="How To Make Friends In Your 30s")

    #     author1 = Author(name="Blu Renolds")
    #     author2 = Author(name="Chip Egan")
    #     author3 = Author(name="Alyssa Wyatt")

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
    return {"success": f"Now going to process your files {filename} whit token : {token}"}
