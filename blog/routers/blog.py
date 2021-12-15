from fastapi import APIRouter, Depends, status, Response
from .. import schemas, database
from sqlalchemy.orm import Session
from typing import List
from ..repository import blogBL

router = APIRouter(
    prefix='/blog',
    tags=['blogs']
)
get_db = database.get_db


@router.get('/', status_code=status.HTTP_200_OK, response_model=List[schemas.showBlog])
def getallblogs(db: Session = Depends(get_db)):
    return blogBL.get_all(db)


@router.post('/', status_code=status.HTTP_201_CREATED)
def create(blog: schemas.Blog, db: Session = Depends(get_db)):
    return blogBL.create(blog, db)


@router.get('/{id}', status_code=status.HTTP_200_OK, response_model=schemas.showBlog)
def showblog(id, response: Response, db: Session = Depends(get_db)):
    return blogBL.show(id, response, db)


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def destroy(id, db: Session = Depends(get_db)):
    return blogBL.delete(id, db)


@router.put('/{id}', status_code=status.HTTP_202_ACCEPTED)
def update(id, blog: schemas.Blog, db: Session = Depends(get_db)):
    return blogBL.update(id, blog, db)
