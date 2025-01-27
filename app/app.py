# examples/standard/app/app.py

from fastapi import FastAPI, Request
from fastapi_auth_jwt import JWTAuthBackend, JWTAuthenticationMiddleware
from app.config import User, AuthenticationSettings
from app.schemas import RegisterSchema, LoginSchema
# Initialize the Authentication Backend
auth_backend = JWTAuthBackend(
    authentication_config=AuthenticationSettings(),
    user_schema=User,
)
# Create FastAPI app and add middleware
app = FastAPI()
app.add_middleware(
    JWTAuthenticationMiddleware,
    backend=auth_backend,
    exclude_urls=["/register", "/login"],
)
Nedo_db= []



@app.post("/register")
async def sign_up(request_data: RegisterSchema):
    # создать юзера в nedo_db
    if request_data.username !="" and request_data.password!="":
        user= User(
            firstname=request_data.firstname,
            surname=request_data.surname,
            patronymic=request_data.patronymic,
            bio=request_data.bio,
            username=request_data.username,
            password=request_data.password           
        )
        Nedo_db.append(user)
    print(Nedo_db)
    return {"message": "User created"}


@app.post("/login")
async def login(request_data: LoginSchema):
    if any([i.username == request_data.username and i.password == request_data.username for i in Nedo_db]):
        print(request_data , "Exists in db" )
    token = await auth_backend.create_token(
        {
            "username": request_data.username,
        }
    )
    return {"token": f"Bearer {token}"}


@app.get("/account")
async def get_profile_info(request: Request):
    exusername: User = request.state.user.username
    for i in Nedo_db:
        if i.username == exusername:return i 

@app.get("/users")
async def get_profile_info(request: Request):
    return {"users": [ {"username":i.username} for i in Nedo_db]}   


__all__ = ["app"]
