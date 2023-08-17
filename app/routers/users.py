from .. import models,schemas, utils
from ..database import get_db
from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session

router = APIRouter(
    prefix= '/users',
    tags= ['users']
)

@router.post("",status_code=status.HTTP_201_CREATED,response_model=schemas.userCreateResponse)
def createUser(user: schemas.createUsers, db: Session = Depends(get_db)):
    
    #hashing the password 
    user.password = utils.hash(user.password)
    newUser = models.Users(**user.model_dump())
    db.add(newUser)
    db.commit()
    db.refresh(newUser)
    
    return newUser

@router.get('/{id}',response_model=schemas.userCreateResponse)
def getUser(id : int, db: Session = Depends(get_db)):
    user = db.query(models.Users).filter(models.Users.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return user