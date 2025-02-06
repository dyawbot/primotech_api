from fastapi import APIRouter, HTTPException, Path, Depends

# from conn import config 
# from app.core import config
from app.db import session
from sqlalchemy.orm import Session
from app.schemas.users import UserSchema, RequestUser, Response
import app.repository.users as user

router = APIRouter()




@router.post('/create')
async def create(request: RequestUser, db:Session=Depends(session.get_db)):
    _result = await user.create_user(db, request.parameter)
    print(_result.code)
    if _result.code != 200:
         raise HTTPException(status_code=_result.code, detail=_result.message)
    else:
        return Response(code=_result.code,status=_result.status,message=_result.message, result=_result.result).dict(exclude_none=True)


@router.get('/')
async def get(db:Session=Depends(session.get_db)):
    _users = user.get_users(db,0,100)
    return Response(code=200, status="Ok", message="Success Fetch All Users", result = _users).dict(exclude_none = True)

@router.get('/{id}')
async def get_by_id(id:int, db:Session = Depends(session.get_db)):
        _users = user.get_user_by_id(db, id)
        return Response(code=200, status="Ok", message="Success getting all the user", result=_users).dict(exclude_none=True)


