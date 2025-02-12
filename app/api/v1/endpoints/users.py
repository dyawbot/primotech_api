from fastapi import APIRouter, HTTPException, Path, Depends

# from conn import config 
# from app.core import config
from app.db import session
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.users import UserSchema, RequestUser, Response
import app.repository.users as user

router = APIRouter()




@router.post('/create')
async def create(request: RequestUser, db:AsyncSession=Depends(session.get_db)):
    _result = await user.create_user(db, request.parameter)
    print(_result.code)
    if _result.code != 200:
         raise HTTPException(status_code=_result.code, detail=_result.message)
    else:
        return Response(code=_result.code,status=_result.status,message=_result.message, result=_result.result).dict(exclude_none=True)


@router.get('/')
async def get(db:AsyncSession=Depends(session.get_db)):
    _result =await user.get_users(db,0,100)
    if _result.code != 200:
        raise HTTPException(status_code= _result.code, detail= _result.message)
    else:
        return Response(code=200, status=_result.status, message=_result.message, result = _result.result).dict(exclude_none = True)

@router.get('/{id}')
async def get_by_id(id:str, db:AsyncSession = Depends(session.get_db)):
  
    _result =await  user.get_user_by_id(db, id)

    if _result.code != 200:
        raise HTTPException(status_code=_result.code, detail=_result.message)
    else:
        return Response(code=200, status=_result.status, message=_result.message, result=_result.result).dict(exclude_none=True)


