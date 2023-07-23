from fastapi import HTTPException, Security, Depends, APIRouter
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session
from starlette import status

from src.auth_tools import Auth
from src.database import get_db
from src.models import User, Post
from src.schemas import CreatePostModel, PatchPostModel

router = APIRouter()
auth_handler = Auth()
security = HTTPBearer()


@router.get('/post/{row_id}')
def get_post(row_id: str, db: Session = Depends(get_db)):
    try:
        post = db.get(Post, row_id)
    except Exception as error:
        print('Error', error)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail='Failed to get post')
    else:
        if post is None:
            raise HTTPException(status_code=400, detail="There is no such 'id'.")
        ans = {
            'id': post.id,
            'author': post.user.name,
            'title': post.title,
            'content': post.content,
            'count_likes': post.count_likes,
        }
        return {'status': 'success', 'message': 'Successfully received', 'post': ans}


@router.get('/post')
def get_posts(db: Session = Depends(get_db)):
    try:
        posts = db.query(Post).all()
    except Exception as error:
        print('Error', error)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail='Failed to get post')
    else:
        if posts is None:
            raise HTTPException(status_code=400, detail="The base is empty")
        ans = [{'id': post.id, 'author': post.user.name, 'title': post.title, 'content': post.content,
                'count_likes': post.count_likes} for post in posts]

        return {'status': 'success', 'message': 'Successfully received', 'posts': ans}


@router.post('/post')
def post_post(post_details: CreatePostModel, credentials: HTTPAuthorizationCredentials = Security(security), db: Session = Depends(get_db)):
    token = credentials.credentials
    if auth_handler.decode_token(token):
        try:
            user_id = db.query(User).filter(User.name == auth_handler.decode_token(token)).first().id
            post = Post(user_id=user_id, count_likes=0, **post_details.dict())
            db.add(post)
            db.commit()
            db.refresh(post)
        except Exception as error:
            print('Error', error)
            db.rollback()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail='Failed to post')
        else:
            ans = {
                'id': post.id,
                'author': post.user.name,
                'title': post.title,
                'content': post.content,
                'count_likes': post.count_likes
            }
            return {'status': 'success', 'message': 'Successfully placed', 'post': ans}


@router.patch('/post/{row_id}')
def patch_post(row_id: str, post_details: PatchPostModel, credentials: HTTPAuthorizationCredentials = Security(security), db: Session = Depends(get_db)):
    token = credentials.credentials
    if auth_handler.decode_token(token):
        post = db.get(Post, row_id)
        if post is None:
            raise HTTPException(status_code=400, detail="There is no such 'id'.")
        user_id = db.query(User).filter(User.name == auth_handler.decode_token(token)).first().id
        if user_id != post.user_id:
            raise HTTPException(status_code=403, detail="You don't have access to this post.")
        try:
            post.title = post_details.title if post_details.title is not None else post.title
            post.content = post_details.content if post_details.content is not None else post.content
            db.commit()
            db.refresh(post)
        except Exception as error:
            print('Error', error)
            db.rollback()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail='Failed to patch')
        else:
            ans = {
                'id': post.id,
                'author': post.user.name,
                'title': post.title,
                'content': post.content,
                'count_likes': post.count_likes
            }
            return {'status': 'success', 'message': 'Successfully changed', 'post': ans}


@router.delete('/post/{row_id}')
def delete_post(row_id: str, credentials: HTTPAuthorizationCredentials = Security(security), db: Session = Depends(get_db)):
    token = credentials.credentials
    if auth_handler.decode_token(token):
        post = db.get(Post, row_id)
        if post is None:
            raise HTTPException(status_code=400, detail="There is no such 'id'.")
        user_id = db.query(User).filter(User.name == auth_handler.decode_token(token)).first().id
        if user_id != post.user_id:
            raise HTTPException(status_code=403, detail="You don't have access to this post.")
        try:
            db.delete(post)
            db.commit()
            db.refresh(post)
        except Exception as error:
            print('Error', error)
            db.rollback()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail='Failed to delete')
        else:
            return {'status': 'success', 'message': 'Successfully deleted'}