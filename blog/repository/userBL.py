from .. import models, schemas
from sqlalchemy.orm import Session
from fastapi import status, Response, HTTPException
from ..hashing import Hash

def create(user: schemas.User, db: Session):
    new_user = models.User(username=user.username,
                           email=user.email, password=Hash.bcrypt(user.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def show(id, db: Session):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"user {id} not found")
    return user
