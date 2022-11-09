from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationships

from .database import Base

# book_id     varchar(255)  NO         <null>
# book_name   varchar(255)  YES        <null>
# is_url      tinyint(1)    NO         0
# book_pages  int(11)       NO         <null>
# path        varchar(510)  YES        <null>
# css         text          YES        <null>

class Books(Base):
    __tablename__ = "bms_view_inputs"
#  id = Column(Integer, primary_key=True, index=True)
    book_id = Column(Integer)
    book_name = Column(String)
    is_url = Column(Boolean, default=False)
    book_pages = Column(Integer)
    path = Column(String)
    css = Column(String)

 #   items = relationships("Item", back_populates="owner")


#bms_inputs_ctrls_id  int(10) unsigned  NO         0
#bms_books_id         int(10) unsigned  NO         0
#bms_bookpages_id     int(10) unsigned  NO         0
#label                mediumtext        YES        <null>
#user_id              int(10) unsigned  NO         0
#attribute            varchar(255)      YES        <null>
#value                mediumtext        YES        <null>


class Forms(Base):
    __tablename__ = "bms_view_users_inputs"
    bms_inputs_ctrls_id = (Integer)
    bms_books_id = (Integer)      
    bms_bookpages_id = (Integer)
    label = (String)
    user_id = (Integer)
    attribute = (String)
    value = (String)
#    id = Column(Integer, primary_key=True, index=True)
#    title = Column(String, index=True)
#    description = Column(String, index=True)
#    owner_id = Column(Integer, ForeignKey("users.id"))

 #   owner = relationships("User", back_populates="items")
