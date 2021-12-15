from fastapi import APIRouter, Depends, status, Response, HTTPException
from .. import schemas, database, models
from sqlalchemy.orm import Session
from typing import List


router = APIRouter(
    tags=['blogs']
)
get_db = database.get_db


@router.get('/blog', status_code=status.HTTP_200_OK, response_model=List[schemas.showBlog])
def getallblogs(db: Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return blogs


@router.post('/blog', status_code=status.HTTP_201_CREATED)
def create(blog: schemas.Blog, db: Session = Depends(get_db)):
    new_blog = models.Blog(title=blog.title, body=blog.body, user_id=1)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


@router.get('/blog/{id}', status_code=status.HTTP_200_OK, response_model=schemas.showBlog)
def showblog(id, response: Response, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Blog with id {id} is not available")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {'datail': f"Blog with id {id} is not available"}
    return blog


@router.delete('/blog/{id}', status_code=status.HTTP_204_NO_CONTENT)
def destroy(id, db: Session = Depends(get_db)):
    db_blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not db_blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'blog {id} not found, create it first')
    db_blog.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put('/blog/{id}', status_code=status.HTTP_202_ACCEPTED)
def update(id, blog: schemas.Blog, db: Session = Depends(get_db)):
    db_blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not db_blog.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f'blog {id} not found, create it first')
    db_blog.update(blog.dict())
    db.commit()
    return blog
