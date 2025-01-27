from fastapi import FastAPI, Request
from fastapi.responses import FileResponse, RedirectResponse
from fastapi_auth_jwt import JWTAuthBackend, JWTAuthenticationMiddleware
from app.config import User, AuthenticationSettings
from app.schemas import RegisterSchema, LoginSchema
auth_backend = JWTAuthBackend(
    authentication_config=AuthenticationSettings(),
    user_schema=User,
)
app = FastAPI()
app.add_middleware(
    JWTAuthenticationMiddleware,
    backend=auth_backend,
    exclude_urls=["/register", "/login","/"],
)
Nedo_db= []



@app.post("/register")
async def sign_up(request_data: RegisterSchema):
    # создать юзера в nedo_db
    if request_data.username !="" and request_data.password!="":
        if not any([i.username == request_data.username  for i in Nedo_db]):
            user= User(
                firstname=request_data.firstname,
                surname=request_data.surname,
                patronymic=request_data.patronymic,
                group=request_data.group,
                bio=request_data.bio,
                username=request_data.username,
                password=request_data.password           
            )
            Nedo_db.append(user)
        else:
            return {"message":"Try other username"}
    print(Nedo_db)
    return {}


@app.post("/login")
async def login(request_data: LoginSchema):
    if any([i.username == request_data.username and i.password == request_data.password for i in Nedo_db]):
        token = await auth_backend.create_token(
            {
                "username": request_data.username,
            }
        )
        return {"token": f"{token}"}
    else:return{"message":"Invalid pass or login"}


@app.get("/account") # Проблема в либе ( в request.state 50/50 есть-нету user class)
async def get_profile_info(request: Request):
    user: User = request.state.user.username # tried => # user = request.state.user.username # user = request.state.username
    for i in Nedo_db:
        if i.username == user:
            return {
                "surname" : i.surname,
                "firstname" : i.firstname,
                "patronymic": i.patronymic,
                "group":i.group,
                "bio": i.bio,
                "username":i.username
            } 

@app.get("/users")
async def get_users(request: Request):
    print(Nedo_db)
    return {"users": [ {"surname":i.surname,"group":i.group} for i in Nedo_db]}   




# frontend 

@app.get("/login")
def login_serve():
    return FileResponse("app/static/login.html")
@app.get("/register")
def reg_serve():
    return FileResponse("app/static/register.html")

@app.get("/account.html")
def acc_serve():
    return FileResponse("app/static/account.html")
@app.get("/users.html")
def users_serve():
    return FileResponse("app/static/users.html")



@app.get("/")
def root():
    return RedirectResponse(url='/login')
__all__ = ["app"]