from pydantic import BaseModel
from typing import List


class BlogBase(BaseModel):
    title: str
    body: str


class Blog(BlogBase):
    class Config():
        orm_mode = True


class User(BaseModel):
    username: str
    email: str
    password: str


class showUserToBlog(BaseModel):
    username: str
    email: str

    class Config():
        orm_mode = True


class showUser(showUserToBlog):
    blogs: List[Blog]

    class Config():
        orm_mode = True


class showBlog(BaseModel):
    title: str
    body: str
    creator: showUserToBlog

    class Config():
        orm_mode = True
