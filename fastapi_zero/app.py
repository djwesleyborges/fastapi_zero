from http import HTTPStatus

from fastapi import Depends, FastAPI, HTTPException
from requests import Session
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from fastapi_zero.database import get_session
from fastapi_zero.models import User
from fastapi_zero.schema import (
    Message,
    UserListSchema,
    UserPublicSchema,
    UserSchema,
)

app = FastAPI(title='FastAPI Zero')

database = []


@app.get('/', response_model=Message, status_code=HTTPStatus.OK)
def read_root():
    return {'message': 'Welcome to FastAPI Zero!'}


@app.post(
    '/users/', status_code=HTTPStatus.CREATED, response_model=UserPublicSchema
)
def create_user(user: UserSchema, session: Session = Depends(get_session)):

    db_user = session.scalar(
        select(User).where(
            (User.username == user.username) | (User.email == user.email)
        )
    )

    if db_user:
        if db_user.username == user.username:
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT,
                detail='Username already exists',
            )
        elif db_user.email == user.email:
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT, detail='Email already exists'
            )
    db_user = User(
        username=user.username, email=user.email, password=user.password
    )

    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user


@app.get('/users/', response_model=UserListSchema, status_code=HTTPStatus.OK)
def get_users(
    limit: int = 10, offset: int = 0, session: Session = Depends(get_session)
):
    users = session.scalars(select(User).limit(limit).offset(offset))
    return {'users': users}


@app.put(
    '/users/{user_id}',
    response_model=UserPublicSchema,
    status_code=HTTPStatus.OK,
)
def update_user(
    user_id: int, user: UserSchema, session: Session = Depends(get_session)
):
    user_db = session.scalar(select(User).where(User.id == user_id))
    if not user_db:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='User not found'
        )

    user_db.username = user.username
    user_db.email = user.email
    user_db.password = user.password

    session.add(user_db)

    try:
        session.commit()
    except IntegrityError:
        session.rollback()
        raise HTTPException(
            detail='Username or email already exists',
            status_code=HTTPStatus.CONFLICT,
        )
    session.refresh(user_db)
    return user_db


@app.delete(
    '/users/{user_id}', status_code=HTTPStatus.OK, response_model=Message
)
def delete_user(user_id: int, session: Session = Depends(get_session)):
    user_db = session.scalar(select(User).where(User.id == user_id))
    if not user_db:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='User not found'
        )

    session.delete(user_db)
    session.commit()
    return {'message': 'User deleted'}
