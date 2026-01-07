from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.dependencies import get_webudget_db
from app.schemas.webudget.users.user_requesters import LoginRequest
from app.schemas.webudget.users.login_response import LoginResponse
from app.schemas.webudget.users.users_shema import UserRegistrationShema
from app.schemas.UserSchemas.users import Response
from app.repository.webudget import user_repo

from fastapi.templating import Jinja2Templates
from fastapi import APIRouter, Depends, HTTPException, Request,status, Response as ResponseFastAPI




from app.repository.webudget.helpers import verify_token
from app.repository.webudget.user_repo import activate_email as activate

user_router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@user_router.post('/login')
async def login(request: LoginRequest,
                 response: ResponseFastAPI,
                 db:AsyncSession=Depends(get_webudget_db)):

    _result = await user_repo.user_login(db,request)
    if _result.code != status.HTTP_200_OK:
         raise HTTPException(status_code=_result.code, detail=_result.message)
    else:
        response.headers["X-Token"] = f"{_result.token}"
        print(_result.result["exp"])
        return LoginResponse(expiration=str(_result.result["exp"]), token=_result.result["access_token"] ).dict(exclude_none=True)
        # return LoginResponse(status=_result.status,message=_result.message, result=_result.result).dict(exclude_none=True) 

@user_router.post('/register')
async def create(request: UserRegistrationShema, db:AsyncSession=Depends(get_webudget_db)):
    #repos here
    _result = await user_repo.user_registration(db,request)
    print(_result)
    if _result.code != status.HTTP_201_CREATED:
         raise HTTPException(status_code=_result.code, detail=_result.message)
    else:
        return Response(code=_result.code,status=_result.status,message=_result.message, result=_result.result).dict(exclude_none=True)

@user_router.get("/me")
async def verification_webudget(id:str, request: Request, db: AsyncSession = Depends(get_webudget_db)):

    verified_email= verify_token(id)
    
    if not isinstance(verified_email, str):
                print(type(verified_email))
                return verified_email
    _result = await activate(db=db,email=verified_email)

    if _result.code != 200:
        raise HTTPException(status_code=_result.code, detail=_result.message)
    else:
        return templates.TemplateResponse("email_verified.html", {
        "request": request,
        "message": _result.message
    })