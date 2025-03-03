from fastapi import APIRouter, File, UploadFile, Form, Depends, HTTPException
from fastapi.responses import FileResponse

from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated
from app.repository import images
from app.db import session
from app.model.helper import UserImageHelper
from app.core.config import UPLOAD_DIR
from app.schemas.users import  RequestUser, Response
from app.utils.removed_characters import clean_string as cs
import os
import hashlib



image_router = APIRouter()


def get_hashed_key(user_id: str) -> str:
    return hashlib.sha256(user_id.encode()).hexdigest()[:8] 


@image_router.post('/')
async def get(username: Annotated[str, Form()], db: Session=Depends(session.get_db)):
    _images =await images.get_user_id_by_user_id(db,username)
    return _images

@image_router.get('/{id}/{filename}')
async def get_image_by_id(id: str, filename: str):
    # user_hash = get_hashed_key(id)  
    user_folder = os.path.join(UPLOAD_DIR, id)
    file_path = os.path.join(user_folder, filename)
    print(file_path)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Image not found")
    return FileResponse(file_path)  

@image_router.get('/by-images')
async def get_all_image_by_id(id:str, db: AsyncSession = Depends(session.get_db)):
    result = await images.get_image_by_id_repo(db=db, username=id)

    if result.code != 200:
        raise HTTPException(status_code=result.code, detail=result.message)
    else:
        return Response(code=result.code,status=result.status, message=result.message, result=result.result).dict(exclude_none=True)





@image_router.post('/upload')
async def upload_images(username: Annotated[str, Form()], file: UploadFile = File(...), db: AsyncSession = Depends(session.get_db)):
    # user_hashed = get_hashed_key(username)
    filename = file.filename
    filename = cs(filename)
    file_extension = filename.split(".")[-1].lower()
    user_folder = UPLOAD_DIR / str(username)
    allow_image_extension = ["png", "jpeg", "jpg"]
    user_folder.mkdir(parents=True, exist_ok=True) 
    
    if file_extension not in allow_image_extension:
        raise HTTPException(status_code=400, detail="File type must be PNG, JPEG or JPG")
    
    file_path = user_folder / filename
    with open(file_path, "wb") as f:
        content = await file.read()  
        f.write(content)  

    image_schema = UserImageHelper(username=username, image_name=filename, image_url=f"/images/{username}/{filename}")
    response =await images.save_image_data(db, image_schema)
   

    if response.code != 200:
        raise HTTPException(status_code=response.code, detail=response.message)
    else:
        return Response(code=response.code,status=response.status, message=response.message, result=response.result).dict(exclude_none=True)
    
    
