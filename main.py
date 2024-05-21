from pathlib import Path
import tempfile
from fastapi import FastAPI, File, UploadFile, Request
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from rembg import remove
app = FastAPI()

templates = Jinja2Templates(directory=".")

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("form.html", {"request": request})

@app.post("/rmbg")
async def remove_background(file: UploadFile = File(...)):
    if file.content_type.startswith('image/'):
        input_data = await file.read()
        output_data = remove(input_data)
        
        # Save output data to a temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix='.png', mode='wb+') as tmp:
            tmp.write(output_data)
            tmp_path = tmp.name
    
        return FileResponse(path=tmp_path, media_type="image/png", filename=f"{Path(file.filename).stem}_rmbg.png")
    else:
        return {"error": "Invalid file type"}