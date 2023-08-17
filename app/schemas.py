from pydantic import BaseModel,EmailStr
from typing import Optional
from datetime import datetime

class PostBase(BaseModel):
    title: str
    content: str
    isChildSafe: bool = False
    rating: Optional[int] = None
    
class PostCreate(PostBase):
    pass 

class userCreateResponse(BaseModel):
    email: EmailStr
    created_at: datetime
    
    class Config:
        from_attributes = True
        
class Post(BaseModel):
    title: str
    content: str
    owner_id : int
    id: int
    owner: userCreateResponse
    class Config:
        from_attributes = True
        
class createUsers(BaseModel):
    email: EmailStr
    password: str
    
        
class userLogin(BaseModel):
    email: EmailStr
    password: str
    
class Token(BaseModel):
    accessToken: str
    tokenType: str
    
class Tokendata(BaseModel):
    id: str
    
class Vote(BaseModel):
    post_id: int
    dir :  int
    
class PostOut(BaseModel):
    posts:Post
    votes: int
    class Config:
        from_attributes = True