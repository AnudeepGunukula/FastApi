from fastapi import APIRouter, Depends, status, Response, HTTPException
from .. import schemas, database, models
from sqlalchemy.orm import Session
from typing import List
from ..hashing import Hash

router = APIRouter(
    tags=['users']
)
get_db = database.get_db


@router.post('/user', response_model=schemas.showUser)
def create_user(user: schemas.User, db: Session = Depends(get_db)):
    new_user = models.User(username=user.username,
                           email=user.email, password=Hash.bcrypt(user.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.get('/user/{id}', response_model=schemas.showUser)
def get_user(id, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"user {id} not found")
    return user
