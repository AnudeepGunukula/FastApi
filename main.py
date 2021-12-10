from fastapi import FastAPI
from typing import Optional
from pydantic import BaseModel

app = FastAPI()


@app.get('/blog')
# default params is 10 and True
def index(limit: int = 10, published: bool = True, sort: Optional[str] = None):
    # query param limit
    if published:
        return {'data': f'{limit} published blogs from db'}
    else:
        return {'data': f'{limit} blogs from db'}


@app.get('/blog/unpublished')
def unpublished():
    return {'data': 'all unpublished blogs'}


@app.get('/blog/{id}')   # id taken from route
def show(id: int):
    return {'data': id}


@app.get('/blog/{id}/comments')
def comments(id, limit=10):        # here id takes from path and limit takes from query params
    return {'data': f"id is {id} and limit is {limit}"}


class Blog(BaseModel):
    title: str
    body: str
    published: Optional[bool]


@app.post('/blog')
def create_blog(blog: Blog):
    return {'data': f'Blog is created with title {blog.title} and its body is {blog.body} '}
    # return {'data': "Blog is Created"}
