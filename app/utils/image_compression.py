from fastapi import UploadFile
from PIL import Image
from io import BytesIO
from pathlib import Path


async def image_compression(file: UploadFile, file_name: str, file_path: str):

    if(file is None):
        print("NO IMAGES")
    await file.seek(0) 
    image_bytes = await file.read()

    try:
        image = Image.open(BytesIO(image_bytes))

        image = image.convert("RGB")
        max_dimension = 1280
        if max(image.size) > max_dimension:
            image.thumbnail((max_dimension, max_dimension), Image.LANCZOS)

            compressed_filename = Path(file_name).stem  + ".jpg"
            save_path = file_path / compressed_filename
            image.save(save_path, "jpeg", quality=25, optimizer=True)
            print(f"Image saved to: {save_path} - size: {save_path.stat().st_size / 1024:.2f}KB")

    except Exception as e:
        print(e)
        # raise HTTPException(status_code=500, detail=f"Image processing error: {str(e)}")

