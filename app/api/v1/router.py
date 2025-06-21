from fastapi import APIRouter, Depends
from app.api.v1 import authentications
from app.api.v1.endpoints import users, images, e_verification


api_router = APIRouter()   


api_router.include_router(users.router, prefix="/users", tags=["users"])    
api_router.include_router(images.image_router, prefix="/images", tags=["images"]) 
api_router.include_router(e_verification.router, prefix="/activate", tags=["verification"])


#protected
api_router.include_router(images.protected_router, prefix="/images", tags=["images-protected"])