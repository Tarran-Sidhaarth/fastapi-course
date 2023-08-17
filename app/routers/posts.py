from .. import models,schemas,oauth2
from ..database import get_db
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import Any,List,Optional

router = APIRouter(
    prefix = '/posts',
    tags= ['posts']
)

@router.get("") # ,response_model = List[schemas.PostOut])
def getPosts(db: Session = Depends(get_db),currUser: str = Depends(oauth2.currentUser),search: Optional[str]=""):
    # cursor.execute('''select * from posts''')
    # posts = cursor.fetchall()
    posts = db.query(models.Post).filter(models.Post.title.contains(search))
    nvotes =db.query(func.count(models.Votes.post_id)).filter(models.Votes.post_id == models.Post.id).group_by(models.Post.id).subquery().select().scalar()
    return posts.all()


@router.get("/{id}",response_model = schemas.Post)
def getPost(id: int, response:Response,db: Session = Depends(get_db),currUser: str = Depends(oauth2.currentUser)):
    # cursor.execute("""select * from posts where id  =%s;""",(str(id)))
    # retrievedPost = cursor.fetchone()
    retrievedPost = db.query(models.Post).filter(models.Post.id == id).first()
    if not retrievedPost:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,detail=f"could not find post id:{id}")
        # response.status_code = status.HTTP_404_NOT_FOUND
    return retrievedPost

@router.post("",response_model=schemas.Post, status_code=status.HTTP_201_CREATED)
def createPosts(newPost: schemas.PostCreate,db: Session = Depends(get_db),currUser: str = Depends(oauth2.currentUser)):
    # cursor.execute("""INSERT INTO posts (title, content, isChildSafe, rating) VALUES (%s,%s,%s,%s) returning *;""",(newPost.title,newPost.content,newPost.isChildSafe,newPost.rating))
    # data = cursor.fetchone()
    # conn.commit()
    print(currUser)
    data = models.Post(**newPost.model_dump(),owner_id =currUser.id)
    db.add(data)
    db.commit()
    db.refresh(data)
    return data

@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
def deletePost(id: int,db: Session = Depends(get_db),currUser: str = Depends(oauth2.currentUser)):
    # cursor.execute("""delete from posts where id = %s""",(str(id)))
    # conn.commit()
    post = db.query(models.Post).filter(models.Post.id == id)
    if post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    if currUser.id != post.first().owner_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    db.delete(post.one())
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.patch("/{id}",status_code=status.HTTP_200_OK)
def updatePost(id:int,updateDetails:schemas.PostCreate, db: Session = Depends(get_db),currUser: str = Depends(oauth2.currentUser)):
    # cursor.execute("""update posts set title = %s, content = %s, isChildSafe = %s, rating = %s where id = %s returning *;""",(updateDetails.title,updateDetails.content,updateDetails.isChildSafe,updateDetails.rating,id))
    # index = cursor.fetchone()
    # conn.commit()
    index = db.query(models.Post).filter(models.Post.id == id)
    post = index.one()
    if index.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"could not find id: {id}")
    for attr, value in updateDetails.model_dump().items():
        setattr(post, attr, value)
    db.commit()
    db.refresh(post)
    return {"message":"successfully updated",
            "data":post}