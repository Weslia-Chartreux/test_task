from fastapi import HTTPException, Security, Depends, APIRouter
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session
from starlette import status

from src.auth_tools import Auth
from src.database import get_db
from src.models import User
from src.schemas import AuthModel


router = APIRouter()
auth_handler = Auth()
security = HTTPBearer()


@router.post('/signup')
def signup(user_details: AuthModel, db: Session = Depends(get_db)):
    if db.query(User).filter(User.name == user_details.name.lower()).first():
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail='Account already exist')
    try:
        hashed_password = auth_handler.encode_password(user_details.password)
        payload = {'name': user_details.name.lower(), 'password': hashed_password}
        new_user = User(**payload)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return {'status': 'success', 'message': 'Thank you for registering!!'}
    except Exception as error:
        print('Error', error)
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail='Failed to signup user')


@router.post('/login')
def login(user_details: AuthModel, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.name == user_details.name.lower()).first()
    if not user:
        return HTTPException(status_code=401, detail='Invalid username')
    if not auth_handler.verify_password(user_details.password, user.password):
        return HTTPException(status_code=401, detail='Invalid password')

    access_token = auth_handler.encode_token(user.name)
    refresh_token = auth_handler.encode_refresh_token(user.name)
    return {'access_token': access_token, 'refresh_token': refresh_token}


@router.get('/refresh_token')
def refresh_token(credentials: HTTPAuthorizationCredentials = Security(security)):
    refresh_token = credentials.credentials
    new_token = auth_handler.refresh_token(refresh_token)
    return {'access_token': new_token}