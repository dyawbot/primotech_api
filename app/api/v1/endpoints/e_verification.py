from fastapi import APIRouter, Depends, HTTPException,status
from fastapi.responses import HTMLResponse
from jose import JWTError
import jwt
from sqlalchemy.ext.asyncio import AsyncSession
from app.db import session
from app.model.helper import StatusHelper
from app.repository.users import ALGORITHM, SECRET_KEY
from app.repository.verification_and_activation import activate_email as activate
from app.schemas.users import Response




router = APIRouter()


def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("email")
        if email is None:
            return StatusHelper(code=status.HTTP_401_UNAUTHORIZED, status= "Error", message= "Invalid token")
        return str(email)
    except JWTError as e:
        print(str(e))
        return StatusHelper(code=status.HTTP_401_UNAUTHORIZED, status= "Error", message= str(e))

@router.get("/me")
async def verify_and_activate_email(id:str, db: AsyncSession = Depends(session.get_db)):

    verified_email= verify_token(id)
    
    if not isinstance(verified_email, str):
                print(type(verified_email))
                return verified_email
    _result = await activate(db=db,email=verified_email)

    if _result.code != 200:
        raise HTTPException(status_code=_result.code, detail=_result.message)
    else:
        # return Response(code=200, status=_result.status, message=_result.message, result= None).dict(exclude_none=True)
          return HTMLResponse(
        content=f"""
            <html>
                <head><title>Email Verified</title></head>
                <body>
                    <h2>🎉 Email Verified Successfully!</h2>
                    <p>{_result.message}</p>
                </body>
            </html>
        """,
        status_code=200
    )