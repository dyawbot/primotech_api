from fastapi import Depends, HTTPException, Request, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError
import jwt




from app.core.config import settings


from app.model.helper import StatusHelper

security = HTTPBearer()

def authenticate_user(request: Request, credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id = payload.get("sub")
        user_email = payload.get(("email"))

        if user_id is None:
            # return StatusHelper(code= 422, status="Error", message="Invalid token payload")
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Invalid token payload"
            )
        if user_email is None:
            raise HTTPException(
                status_code= status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail= "You're email is not verified or registered"
            )
        # return {"user_id": user_id, "email" : user_email}
        request.state.user = {
            "user_id" : user_id,
            "user_email" : user_email
        }

    except Exception as e:
        print(e)
    
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    except JWTError as e:
         print(e)
        # raise HTTPException(status_code=401, detail="Invalid or expired token")
        # return StatusHelper(code= 401, status="Error", message="Invalid or expired token")
         raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    

# def verify_token(token: str):
#     try:
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         username: str = payload.get("sub")
#         if username is None:
#             return StatusHelper(code=status.HTTP_401_UNAUTHORIZED, status= "Error", message= "Invalid token")
#         return str(username)
#     except JWTError as e:
#         print(str(e))
#         return StatusHelper(code=status.HTTP_401_UNAUTHORIZED, status= "Error", message= str(e))
