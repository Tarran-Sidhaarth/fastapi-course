from .. import models,schemas,utils, oauth2
from ..database import get_db
from fastapi import status, HTTPException, Depends, APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

router = APIRouter(tags= ['Authentication'])

@router.post('/login')
def userLogin(credentials:OAuth2PasswordRequestForm = Depends(),db: Session= Depends(get_db)):
    user = db.query(models.Users).filter(models.Users.email == credentials.username).first()
    
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="invalid credentials")
    
    if not utils.verify(credentials.password,user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="invalid credentials")
    
    access_token = oauth2.createToken(data = {"user_Id": user.id})
    return {"token":access_token,"token type":"bearer"}