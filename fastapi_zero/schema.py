from pydantic import BaseModel, EmailStr


class Message(BaseModel):
    message: str


class UserSchema(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserPublicSchema(BaseModel):
    username: str
    email: EmailStr
    id: int


class UserDBSchema(UserSchema):
    id: int


class UserListSchema(BaseModel):
    users: list[UserPublicSchema]
