from pydantic import BaseModel
from typing import Optional

class BookBase(BaseModel):
    title: str
    author: str
    genre: str
    desc: str
    avail_status: str

class BookCreate(BookBase):
    url: str

    class Config:
        orm_mode = True

class BookUpdate(BookBase):
    pass

class Book(BookBase):
    id: int
    url: str
    class Config:
        orm_mode = True
