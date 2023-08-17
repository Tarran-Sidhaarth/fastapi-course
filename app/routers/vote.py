from .. import models,schemas, utils,oauth2
from ..database import get_db
from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session

router = APIRouter(tags=['Votes'],prefix="/vote")

@router.post("",status_code=status.HTTP_201_CREATED)
def vote(vote:schemas.Vote,db: Session = Depends(get_db),currUser: str = Depends(oauth2.currentUser)):
    found = db.query(models.Votes).filter(models.Votes.post_id == vote.post_id,models.Votes.user_id == currUser.id).first()
    if found:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail=f"already voted")
    if vote.dir > 0:
        new_vote = models.Votes(post_id = vote.post_id,user_id = currUser.id)
        db.add(new_vote)
        db.commit()
        return {"success":"voted"}
    else:
        # if not found:
        #     raise(HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="post doesnt exist"))
        found.delete()
        db.commit()
        return {"deleted":'vote'}