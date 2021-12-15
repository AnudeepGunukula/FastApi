from .. import models, schemas
from sqlalchemy.orm import Session
from fastapi import status, Response, HTTPException


def get_all(db: Session):
    blogs = db.query(models.Blog).all()
    return blogs


def create(blog: schemas.Blog, db: Session):
    new_blog = models.Blog(title=blog.title, body=blog.body, user_id=1)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


def show(id, response: Response, db: Session):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Blog with id {id} is not available")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {'datail': f"Blog with id {id} is not available"}
    return blog


def delete(id, db: Session):
    db_blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not db_blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'blog {id} not found, create it first')
    db_blog.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


def update(id, blog: schemas.Blog, db: Session):
    db_blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not db_blog.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f'blog {id} not found, create it first')
    db_blog.update(blog.dict())
    db.commit()
    return blog
