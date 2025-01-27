# examples/standard/app/schemas.py

from pydantic import BaseModel


# Define request schemas
class RegisterSchema(BaseModel):
    # фио группа логин пароль пол 
    surname : str
    firstname : str
    patronymic: str
    group:str
    bio: str
    username: str
    password: str
    


class LoginSchema(BaseModel):
    username: str
    password: str


__all__ = ["RegisterSchema", "LoginSchema"]
