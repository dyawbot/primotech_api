from fastapi import FastAPI, File, UploadFile
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import os
from pathlib import Path
from conn import temp_db as db
app = FastAPI()
UPLOAD_DIR = Path("uploaded_images")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True) 

app.mount("/static", StaticFiles(directory=UPLOAD_DIR), name="static")

@app.post("/upload/")
async def upload_image(file: UploadFile = File(...)):
   
    filename = file.filename
    file_extension = filename.split(".")[-1].lower()

    
    allowed_extensions = ["png", "jpeg", "jpg"]

    if file_extension not in allowed_extensions:
        return {"error": "File type must be PNG, JPEG, or JPG"}

    # Save the uploaded file
    file_path = UPLOAD_DIR / filename
    with open(file_path, "wb") as f:
        content = await file.read()  
        f.write(content)  
    
    db.add_data("user", filename)
    return {"filename": filename, "path": str(file_path)}



@app.get("/images")
async def get_images_by_id():
    print("get the images strings on db using id")

# HTML form to upload files
@app.get("/", response_class=HTMLResponse)
async def upload_form():
    return """
    <html>
        <body>
            <h2>Upload an image (PNG, JPEG, or JPG)</h2>
            <form action="/upload/" enctype="multipart/form-data" method="post">
                <input name="file" type="file">
                <input type="submit">
            </form>
        </body>
    </html>
    """


# @app.get("/")
# async def read_root():
#     return {"message": "Hello from FastAPI on Project IDX!"}
