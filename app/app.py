import base64
import json
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
    if not any([i.username == request_data.username and i.password == request_data.password for i in Nedo_db]):
        return{"message":"Invalid pass or login"}
    token = await auth_backend.create_token(
        {
            "username": request_data.username,
        }
    )
    return {"token": f"{token}"}


@app.get("/account") 
async def get_profile_info(request: Request):
    #    # Проблема в либе ( в request.state нету user class ) 
    print(vars(request.state),dir(request.state),type(request.state),"\n")
    # Проверены=> 
    # # user = request.state.user 
    # # user = request.state.username 
    # # user = request.state
    # user: User = "request.state.user" 
    
    # unsafe_fix
    jsonfromtoken= str( base64.b64decode(request.headers.get("Authorization").replace("Bearer","").split(".")[1])  ,encoding='utf-8')
    user=json.loads(jsonfromtoken)
    for i in Nedo_db:
        if i.username == user.username:
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