# import datetime
# from datetime import datetime
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, TIMESTAMP, text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.hybrid import hybrid_property
#from sqlalchemy.dialects.mysql import LONGTEXT
from .database import Base


# BMS_BOOKS
#  `id`                      int unsigned not null auto_increment primary key, --
#  `book_id`                 varchar(255) not null , -- --> ex: 228
#  `pages`                   int null, -- --> 8 total pages
#  `book_name`               varchar(255) null, -- --> Guia_UV
#  `is_url`          bool not null default false, -- --> means false is path url/{book_id} else url?book_id={id}&var=foo
#  `created`                 datetime,
#  `modified`                datetime,
#  `status`                  bool not null default true


class Upload(Base):
    __tablename__ = "bms_controls_files"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True)
    labelname = Column(String, index=True)
    file_name = Column(String, index=True)
    pathname = Column(String, index=True)
    extname = Column(String, index=True)
    md5sum = Column(String, index=True)
    file_size = Column(String, index=True)
    atime = Column(String, index=True)
    mtime = Column(String, index=True)
    ctime = Column(String, index=True)
    username = Column(String, index=True)
    datetime_login = Column(String, index=True)
    ip_remote = Column(String, index=True)
    created = Column(TIMESTAMP, nullable=False, server_default=func.now())
    modified = Column(DateTime, server_default=text(
        "CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))
    status = Column(Boolean, default=True)


class File(Base):
    __tablename__ = "bms_books"
    id = Column(Integer, primary_key=True, index=True)
    book_id = Column(Integer)
    pages = Column(Integer)
    book_name = Column(String)
    is_url = Column(Boolean, default=False)
    created = Column(TIMESTAMP, nullable=True, server_default=func.now())
    modified = Column(DateTime, server_default=text(
        "CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))
    status = Column(Boolean, default=True)


class Item(Base):
    __tablename__ = "bms_cache_books"

    id = Column(Integer, primary_key=True, index=True)
    book_id = Column(Integer, index=True)
    pages = Column(Integer)
    book_name = Column(String, index=True)
    is_url = Column(Boolean, default=False)
    user_id = Column(Integer, index=True)
    created = Column(TIMESTAMP, nullable=False, server_default=func.now())
#    modified = Column(DateTime, server_default=text(
#        "CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))
#   status = Column(Boolean, default=True)

#    pagination = relationship("Page", back_populates="book")
    pagination = relationship("Page"
                              #                              ,primaryjoin="and_(Item.book_id==Page.bms_books_id)"
                              )
    positions = relationship("Position"
                             #                             ,primaryjoin="and_(Item.book_id==Position.bms_books_id,Page.id==Position.bms_bookpages_id)"
                             )
    inputs = relationship("Input"
                          #                          ,primaryjoin="and_(Item.book_id==Input.bms_books_id,Page.id==Position.bms_bookpages_id)"
                          )
    inpages = relationship("Inpage",
                           secondary="outerjoin(Input,Inpage,Input.id==Inpage.bms_inputs_ctrls_id)"
                           )
    invalues = relationship("Invalue",
                            secondary="outerjoin(Input,Invalue,Input.id==Invalue.bms_inputs_ctrls_id,Item.user_id==Invalue.user_id)"
                            )


class Page(Base):
    __tablename__ = "bms_bookpages"

    id = Column(Integer, primary_key=True, index=True)
    bms_books_id = Column(Integer,  ForeignKey("bms_cache_books.book_id"))
    book_pages = Column(Integer)
    basename = Column(String, index=True)
    pathname = Column(String, index=True)
    created = Column(TIMESTAMP, nullable=False, server_default=func.now())
    modified = Column(DateTime, server_default=text(
        "CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))
    status = Column(Boolean, default=True)

    @hybrid_property
    def path(self):
        return self.basename + self.pathname


class Position(Base):
    __tablename__ = "bms_positions"

    id = Column(Integer, primary_key=True, index=True)
    bms_books_id = Column(Integer,  ForeignKey("bms_cache_books.book_id"))
    bms_bookpages_id = Column(Integer,  ForeignKey("bms_bookpages.id"))
    page = Column(Integer)
    tagpath = Column(String, index=True)
    tag = Column(String, index=True)
    top = Column(String, index=True)
    left = Column(String, index=True)
    width = Column(String, index=True)
    css = Column(String, nullable=True)
    created = Column(TIMESTAMP, nullable=False, server_default=func.now())
    modified = Column(DateTime, server_default=text(
        "CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))
    status = Column(Boolean, default=True)

# NOTE https://docs.sqlalchemy.org/en/14/orm/basic_relationships.html
# https://stackoverflow.com/questions/68626930/fastapi-many-to-many-response-schema-and-relationship
# https://stackoverflow.com/questions/68394091/fastapi-sqlalchemy-pydantic-%E2%86%92-how-to-process-many-to-many-relations


class SourcePositions(Base):
    __tablename__ = "bms_src_positions"

    id = Column(Integer, primary_key=True, index=True)
    bms_books_id = Column(Integer,  ForeignKey("bms_cache_books.book_id"))
    bms_bookpages_id = Column(Integer,  ForeignKey("bms_bookpages.id"))
    color = Column(String, index=True)
    lineWidth = Column(Integer)
    source_width = Column(String, index=True)
    source_height = Column(String, index=True)
    inputType = Column(String, index=True)
    page = Column(Integer)
    x1 = Column(Decimal(18,6))
    y1 = Column(Decimal(18,6))
    x2 = Column(Decimal(18,6))
    y2 = Column(Decimal(18,6))
    created = Column(TIMESTAMP, nullable=False, server_default=func.now())
    modified = Column(DateTime, server_default=text(
        "CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))
    status = Column(Boolean, default=True)


class Input(Base):
    __tablename__ = "bms_inputs_ctrls"

    id = Column(Integer, primary_key=True, index=True)
    bms_books_id = Column(Integer,  ForeignKey("bms_cache_books.book_id"))
    bms_bookpages_id = Column(Integer,  ForeignKey("bms_bookpages.id"))
    label = Column(String, index=True)
    created = Column(TIMESTAMP, nullable=False, server_default=func.now())
    modified = Column(DateTime, server_default=text(
        "CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))
    status = Column(Boolean, default=True)


class Inpage(Base):
    __tablename__ = "bms_inputs_pages"

    id = Column(Integer, primary_key=True, index=True)
    bms_inputs_ctrls_id = Column(Integer,  ForeignKey("bms_inputs_ctrls.id"))
    attribute = Column(String, index=True)
    value = Column(String, index=True)
    created = Column(TIMESTAMP, nullable=False, server_default=func.now())
    modified = Column(DateTime, server_default=text(
        "CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))
    status = Column(Boolean, default=True)


class Invalue(Base):
    __tablename__ = "bms_inputs_values"

    id = Column(Integer, primary_key=True, index=True)
    bms_inputs_ctrls_id = Column(Integer,  ForeignKey("bms_inputs_ctrls.id"))
    user_id = Column(Integer, index=True)
    attribute = Column(String, index=True)
    value = Column(String, index=True)
    created = Column(TIMESTAMP, nullable=False, server_default=func.now())
    modified = Column(DateTime, server_default=text(
        "CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))
    status = Column(Boolean, default=True)


# class User(Base):
#    __tablename__ = "users"
#
#    id = Column(Integer, primary_key=True, index=True)
#    email = Column(String, unique=True, index=True)
#    hashed_password = Column(String)
#    is_active = Column(Boolean, default=True)
#
#    items = relationship("Item", back_populates="owner")
#
#
# class Item(Base):
#    __tablename__ = "items"
#
#    id = Column(Integer, primary_key=True, index=True)
#    title = Column(String, index=True)
#    description = Column(String, index=True)
#    owner_id = Column(Integer, ForeignKey("users.id"))
#
#    owner = relationship("User", back_populates="items")
#
