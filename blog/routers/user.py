from fastapi import APIRouter, Depends
from .. import schemas, database
from sqlalchemy.orm import Session
from ..repository import userBL

router = APIRouter(
    prefix='/user',
    tags=['users']
)
get_db = database.get_db


@router.post('/', response_model=schemas.showUser)
def create_user(user: schemas.User, db: Session = Depends(get_db)):
    return userBL.create(user, db)


@router.get('/{id}', response_model=schemas.showUser)
def get_user(id, db: Session = Depends(get_db)):
    return userBL.show(id, db)
