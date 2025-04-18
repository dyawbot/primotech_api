#you can't rename the image name. cause what if there's a duplicate name from gallery the computation of an image might affected
#unless you compared the images if there's a  same serial number

# this will do. we need to encrypt the name of an image with four or 8 letters.

# def image_rename(filename: str):
from fastapi import UploadFile
import hashlib


async def hash_file(file: UploadFile, length: int = 12) -> str:
    # await file.seek(0)  # reset pointer
    content = await file.read()
    hash_object = hashlib.sha256(content)
    return hash_object.hexdigest()[:length]