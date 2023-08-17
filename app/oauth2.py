from jose import JWTError, jwt
from datetime import datetime, timedelta
from . import schemas,database,models,config
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer

oauth2Scheme = OAuth2PasswordBearer(tokenUrl='login')

#parametrs:
#secret key
#algorithm
#expiration time

SECRET_KEY = config.settings.secretKey
ALGORITHM = config.settings.algorithm
ACCESS_TOKEN_EXPIRATION = config.settings.accessTokenExpiration

def createToken(data:dict):
    to_encode = data.copy()
    expire = datetime.utcnow() +timedelta(minutes=ACCESS_TOKEN_EXPIRATION)
    to_encode.update({'exp':expire})

    enocdedJwt = jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)

    return enocdedJwt

def verifyToken(token:str, credentials_exception):
    try:
        payload = jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        id = str(payload.get('user_Id'))
        if id is None:
            raise credentials_exception
        tokenData = schemas.Tokendata(id=id)
    except JWTError:
        raise credentials_exception
    
    return tokenData
    
def currentUser(token: str = Depends(oauth2Scheme), db: Session = Depends(database.get_db)):
    
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail='could not validate credentials',headers={"WWW-Authenticate": "Bearer"})
    token = verifyToken(token,credentials_exception)
    user = db.query(models.Users).filter(models.Users.id == token.id).first()
    
    return user