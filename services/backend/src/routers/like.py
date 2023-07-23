from fastapi import HTTPException, Security, Depends, APIRouter
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session
from starlette import status

from src.auth_tools import Auth
from src.database import get_db
from src.models import User, Post, Like


router = APIRouter()
auth_handler = Auth()
security = HTTPBearer()


@router.post('/post/like/{row_id}')
def like_post(row_id: str, credentials: HTTPAuthorizationCredentials = Security(security), db: Session = Depends(get_db)):
    token = credentials.credentials
    if auth_handler.decode_token(token):
        post = db.get(Post, row_id)
        if post is None:
            raise HTTPException(status_code=400, detail="There is no such 'id'.")
        user_id = db.query(User).filter(User.name == auth_handler.decode_token(token)).first().id
        like = db.query(Like).filter(Like.user_id == user_id and Like.post_id == row_id).all()
        if like:
            raise HTTPException(status_code=405, detail="You have already liked this post.")
        try:
            new_like = Like(user_id=user_id, post_id=row_id)
            db.add(new_like)
            post.count_likes = post.count_likes + 1
            db.commit()
            db.refresh(new_like)
            db.refresh(post)
        except Exception as error:
            print('Error', error)
            db.rollback()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail='Failed to like')
        else:
            return {'status': 'success', 'message': 'The like has been successfully set.'}


@router.delete('/post/like/{row_id}')
def like_post(row_id: str, credentials: HTTPAuthorizationCredentials = Security(security), db: Session = Depends(get_db)):
    token = credentials.credentials
    if auth_handler.decode_token(token):
        post = db.get(Post, row_id)
        if post is None:
            raise HTTPException(status_code=400, detail="There is no such 'id'.")
        user_id = db.query(User).filter(User.name == auth_handler.decode_token(token)).first().id
        like = db.query(Like).filter(Like.user_id == user_id and Like.post_id == row_id).first()
        if not like:
            raise HTTPException(status_code=405, detail="You didn't like this post.")
        try:
            db.delete(like)
            post.count_likes = post.count_likes - 1
            db.commit()
            db.refresh(post)
        except Exception as error:
            print('Error', error)
            db.rollback()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail='Failed to like')
        else:
            return {'status': 'success', 'message': 'Your like has been successfully deleted.'}