#import datetime
#from datetime import datetime
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, TIMESTAMP, text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declarative_base
from .database import Base

#  `id`                      int unsigned not null auto_increment primary key, -- --> Cual es el pedo?
#  `book_id`                 varchar(255) not null , -- --> ex: 228
#  `pages`                   int null, -- --> 8 total pages
#  `book_name`               varchar(255) null, -- --> Guia_UV
#  `is_url`          bool not null default false, -- --> means false is path url/{book_id} else url?book_id={id}&var=foo
#  `created`                 datetime,
#  `modified`                datetime,
#  `status`                  bool not null default true


class Item(Base):
    __tablename__ = "bms_cache_books"

    id = Column(Integer, primary_key=True, index=True)
    book_id = Column(String, index=True)
    pages = Column(Integer)
    book_name = Column(String, index=True)
    is_url = Column(Boolean, default=False)
    user_id = Column(Integer, index=True)
    created = Column(TIMESTAMP, nullable=False, server_default=func.now())
#    modified = Column(DateTime, server_default=text(
#        "CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))
#   status = Column(Boolean, default=True)

    pagination = relationship("Page", back_populates="book")
    bms_inputs = relationship("Input",
                              primaryjoin="and_(Item.user_id==Input.user_id, "
                              "Input.book_id==Item.book_id)")
#    books_id = Column(
#        Integer, ForeignKey("bms_view_users_inputs.book_id"))
#    users_id = Column(
#        Integer, ForeignKey("bms_view_users_inputs.user_id"))
#
#    inputs = relationship("Input", foreign_keys=[books_id])
#    users = relationship(
#        "Input", foreign_keys=[users_id])



class Page(Base):
    __tablename__ = "bms_view_inputs"

    id = Column(String, primary_key=True, index=True)
    book_id = Column(String,  ForeignKey("bms_cache_books.book_id"))
    book_name = Column(String, index=True)
    is_url = Column(Boolean, default=False)
    book_pages = Column(Integer)
    path = Column(String, index=True)
    css = Column(String, nullable=True)

    book = relationship("Item", back_populates="pagination")


class Input(Base):
    __tablename__ = "bms_cache_view_users_inputs"

    id = Column(String, primary_key=True, index=True)
    input_id = Column(Integer)
    book_id = Column(String, ForeignKey("bms_cache_books.book_id"))
    bms_bookpages_id = Column(String)
    label = Column(String, index=True)
    user_id = Column(Integer, ForeignKey("bms_cache_books.user_id"))
    attribute = Column(String, index=True)
    value = Column(String, nullable=True)

#    inputs = relationship("Item", foreign_keys=[user_id,bms_books_id])
  #  reference = relationship("Item", foreign_keys=[bms_books_id])


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
