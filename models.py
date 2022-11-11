from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
#from sqlalchemy.sql import func
import datetime
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
    __tablename__ = "bms_books"

    id = Column(Integer, primary_key=True, index=True)
    book_id = Column(String)
    pages = Column(Integer)
    book_name = Column(String)
    is_url = Column(Boolean, default=False)
#    created = Column(DateTime(timezone=True), server_default=func.now())
#    modified = Column(DateTime(timezone=True), onupdate=func.now())
#    created = Column(DateTime)
#    modified = Column(DateTime)
    created = DateTime(default=datetime.datetime.utcnow)
    modified = DateTime(default=datetime.datetime.utcnow)
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
