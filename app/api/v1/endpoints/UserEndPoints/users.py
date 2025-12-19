from fastapi import APIRouter, HTTPException, Path, Depends, Query, status

# from conn import config 
# from app.core import config
from app.db import session
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.dependencies import get_dev_db
from app.schemas.UserSchemas.users import UserSchema, RequestUser, Response, RequestLoginUser
import app.repository.UserRepository.users as user
from app.utils.conver_model_to_dict import model_to_dict

router = APIRouter()




@router.post('/create')
async def create(request: RequestUser = Depends(RequestUser), db:AsyncSession=Depends(get_dev_db)):

    print(type(db))
    _result = await user.create_user(db,request)
    print(_result.code)
    if _result.code != status.HTTP_201_CREATED:
         raise HTTPException(status_code=_result.code, detail=_result.message)
    else:
        return Response(code=_result.code,status=_result.status,message=_result.message, result=_result.result).dict(exclude_none=True)


@router.get('/')
async def get(db:AsyncSession=Depends(get_dev_db), skip: int = Query(0, alias="page"), limit: int = 5):
    _result =await user.get_users(db,skip,limit)
    if _result.code != 200:
        raise HTTPException(status_code= _result.code, detail= _result.message)
    else:
        return Response(code=status.HTTP_200_OK, status=_result.status, message=_result.message, result = _result.result).dict(exclude_none = True)

@router.get("/user-images")
async def get_user_with_images(db:AsyncSession = Depends(get_dev_db), skip: int = Query(0, alias="page"), limit: int = 5):
    _result = await user.get_all_users_with_images(db=db,image_limit=3, skip=skip, limit=limit)

    if(_result.code != status.HTTP_200_OK ):
        raise HTTPException(status_code=_result.status, message = _result.message)
    else:
        return Response(code=status.HTTP_200_OK, status=_result.status, message= _result.message, result = _result.result).dict(exclude_none= True)

@router.post('/login')
async def login_user(request: RequestLoginUser = Depends(RequestLoginUser), db:AsyncSession = Depends(get_dev_db)):

    _result =await  user.get_user_by_id(db, request.username, request.password, request.token)

    if _result.code != 200:
        raise HTTPException(status_code=_result.code, detail=_result.message)
    else:
        user_data = model_to_dict(_result.result)
        user_data["token"] = _result.token
        return Response(code=200, status=_result.status, message=_result.message, token=_result.token, result=user_data).dict(exclude_none=True)

