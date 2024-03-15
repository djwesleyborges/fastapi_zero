from pydantic import BaseModel, EmailStr


class Message(BaseModel):
    message: str


class UserSchema(BaseModel):
    """
    Esquema para representar um usuário dentro do sistema.

    Este esquema é utilizado para validar dados de usuário em operações como
    cadastro e atualização de informações de perfil.

    Attributes:
    username (str): O nome de usuário único. Deve ser uma string não vazia.
    email (EmailStr): O endereço de email do usuário. Deve ser um email válido.
    password (str): A senha do usuário. Deve ser uma string não vazia, idealmente
    forte e hash-eada antes de armazenar em qualquer lugar seguro.
    """

    username: str
    email: EmailStr
    password: str


class UserPublic(BaseModel):
    id: int
    username: str
    email: EmailStr


class UserDB(UserSchema):
    id: int


class UserList(BaseModel):
    users: [UserPublic]
