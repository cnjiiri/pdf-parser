from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
import fitz  # PyMuPDF

app = FastAPI()

# CORS settings
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/parse-pdf/")
async def parse_pdf(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        doc = fitz.open(stream=contents, filetype="pdf")

        full_text = ""
        for page in doc:
            text = page.get_text("text")
            if text:
                full_text += text + "\n"

        return {
            "file_name": file.filename,
            "text": full_text.strip()
        }
    except Exception as e:
        return {"error": str(e)}
