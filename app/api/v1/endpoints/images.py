from fastapi import APIRouter, File, UploadFile, Form, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Annotated
from app.repository import images
from app.db import session
from app.model.helper import UserImageHelper
from app.core.config import UPLOAD_DIR
from app.schemas.users import  RequestUser, Response






image_router = APIRouter()


@image_router.post('/')
async def get(username: Annotated[str, Form()], db: Session=Depends(session.get_db)):
    print(" ")
    print(" ")
    print(" ")
    print(" ")
    print(username)
    print(" ")
    print(" ")
    print(" ")
    print(" ")
    print(" ")

    _images =await images.get_user_id_by_user_id(db,username)
    return _images

@image_router.post('/upload')
async def upload_images(username: Annotated[str, Form()], file: UploadFile = File(...), db: Session = Depends(session.get_db)):
    filename = file.filename
    file_extension = filename.split(".")[-1].lower()

    allow_image_extension = ["png", "jpeg", "jpg"]


    if file_extension not in allow_image_extension:
        return {"error": "File type must be PNG, JPEG, or JPG"}

    # Save the uploaded file
    file_path = UPLOAD_DIR / filename
    with open(file_path, "wb") as f:
        content = await file.read()  
        f.write(content)  


    image_schema = UserImageHelper(username=username, image_name=filename, image_path=file_path)


    response =await images.save_image_data(db, image_schema)


    if response.code != 200:
        raise HTTPException(status_code=response.code, detail=response.message)
    else:
        return Response(code=response.code,status=response.status, message=response.message, result=response.result)
    
    # db.add_data("user", filename)
    # return {"filename": filename, "path": str(file_path)}
    