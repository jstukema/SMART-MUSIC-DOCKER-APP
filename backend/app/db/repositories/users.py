from typing import Optional

from pydantic import EmailStr
from fastapi import HTTPException, status
from starlette.status import HTTP_400_BAD_REQUEST
from databases import Database

from app.db.repositories.base import BaseRepository
from app.models.smart_user import UserCreate, UserUpdate, UserInDB, UserPublic
from app.services import auth_service

GET_USER_BY_EMAIL_QUERY = """
    SELECT id, "first_name", "middle_name", "last_name", email, email_verified, username, password, salt, "date_of_birth", gender, "user_type", is_active, is_superuser, created_at, updated_at
    FROM users
    WHERE email = :email;
"""

GET_USER_BY_USERNAME_QUERY = """
    SELECT id, "first_name", "middle_name", "last_name", email, email_verified, username, password, salt, "date_of_birth", gender, "user_type", is_active, is_superuser, created_at, updated_at
    FROM users
    WHERE username = :username;
"""

REGISTER_NEW_USER_QUERY = """
    INSERT INTO users (first_name, middle_name, last_name, username, email, password, date_of_birth, gender, user_type, salt)
    VALUES (:first_name, :middle_name, :last_name, :username, :email, :password, :date_of_birth, :gender, :user_type, :salt)
    RETURNING id, first_name, middle_name, last_name, username, email, email_verified, password, date_of_birth, gender, user_type, salt, is_active, is_superuser, created_at, updated_at;
"""


class UsersRepository(BaseRepository):

    def __init__(self, db: Database) -> None:
        super().__init__(db)
        self.auth_service = auth_service

    async def get_user_by_email(self, *, email: EmailStr) -> UserInDB:
        user_record = await self.db.fetch_one(query=GET_USER_BY_EMAIL_QUERY, values={"email": email})

        if not user_record:
            return None

        return UserInDB(**user_record)

    async def get_user_by_username(self, *, username: str) -> UserInDB:
        user_record = await self.db.fetch_one(query=GET_USER_BY_USERNAME_QUERY, values={"username": username})

        if not user_record:
            return None

        return UserInDB(**user_record)

    async def register_new_user(self, *, new_user: UserCreate) -> UserInDB:
        # make sure email isn't already taken
        if await self.get_user_by_email(email=new_user.email):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="That email is already taken. Login with that email or register with another one."
            )

        # make sure username isn't already taken
        if await self.get_user_by_username(username=new_user.username):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="That username is already taken. Please try another one."
            )

        user_password_update = self.auth_service.create_salt_and_hashed_password(
            plaintext_password=new_user.password
        )
        new_user_params = new_user.copy(update=user_password_update.dict())
        created_user = await self.db.fetch_one(query=REGISTER_NEW_USER_QUERY,
                                               values=new_user_params.dict())

        return UserInDB(**created_user)

    async def authenticate_user(self, *, email: EmailStr, password: str) -> Optional[UserInDB]:
        # make sure user exists in db
        user = await self.get_user_by_email(email=email)
        if not user:
            return None
        # if submitted password doesn't match
        if not self.auth_service.verify_password(password=password, salt=user.salt, hashed_pw=user.password):
            return None

        return user
