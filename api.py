from fastapi import FastAPI, File, UploadFile, Form, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from coordinator import coordinate_detection
import os
import tempfile

app = FastAPI(limits={"max_upload_size": 10 * 1024 * 1024}) 

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def get_index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/detect/language")
async def detect_language(audio_file: UploadFile = File(...), ground_truth_language: str = Form(...)):
    try:
        if not audio_file.content_type.startswith("audio/"):
            return [{"provider": "Error", "language": "unknown", "time_taken": 0, "estimated_cost": {"tokens": 0, "dollars": 0}, "status": "failure", "error_message": "Invalid file format"}]

        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp_file:
            content = await audio_file.read()
            tmp_file.write(content)
            tmp_file_path = tmp_file.name

        print(f"Ground truth language: {ground_truth_language}")

        results = await coordinate_detection(tmp_file_path)
        
        os.unlink(tmp_file_path)
        
        return results
    except Exception as e:
        return [{"provider": "Error", "language": "unknown", "time_taken": 0, "estimated_cost": {"tokens": 0, "dollars": 0}, "status": "failure", "error_message": str(e)}]