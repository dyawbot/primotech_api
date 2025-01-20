from fastapi import FastAPI, File, UploadFile
from fastapi.responses import HTMLResponse
import os
from pathlib import Path

app = FastAPI()
UPLOAD_DIR = Path("uploaded_images")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True) 



@app.post("/upload/")
async def upload_image(file: UploadFile = File(...)):
    # Check the file's extension
    filename = file.filename
    file_extension = filename.split(".")[-1].lower()

    # Acceptable file extensions
    allowed_extensions = ["png", "jpeg", "jpg"]

    if file_extension not in allowed_extensions:
        return {"error": "File type must be PNG, JPEG, or JPG"}

    # Save the uploaded file
    file_path = UPLOAD_DIR / filename
    with open(file_path, "wb") as f:
        content = await file.read()  # Read the file content
        f.write(content)  # Write it to the local file system

    return {"filename": filename, "path": str(file_path)}

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
