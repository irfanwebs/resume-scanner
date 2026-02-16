import json

from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse

from app.config import get_settings
from app.models.schemas import AnalysisResult
from app.services.ai_analyser import analyse_resume, analyse_resume_full
from app.services.pdf_parser import extract_text_from_pdf

settings = get_settings()

app = FastAPI(
    title="ResumeAI API",
    description="AI-powered resume screening and feedback",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


@app.post("/api/analyse")
async def analyse(
    resume: UploadFile = File(...),
    job_description: str = Form(...),
):
    """Analyse a resume against a job description. Returns full JSON result."""

    # Validate file type
    if not resume.filename or not resume.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported")

    # Validate file size
    contents = await resume.read()
    max_bytes = settings.max_file_size_mb * 1024 * 1024
    if len(contents) > max_bytes:
        raise HTTPException(
            status_code=400,
            detail=f"File too large. Maximum size is {settings.max_file_size_mb}MB",
        )

    # Validate job description
    if not job_description.strip():
        raise HTTPException(status_code=400, detail="Job description is required")

    # Extract text from PDF
    try:
        resume_text = extract_text_from_pdf(contents)
    except Exception:
        raise HTTPException(
            status_code=400,
            detail="Could not parse PDF. Please ensure it's a valid PDF file.",
        )

    if not resume_text.strip():
        raise HTTPException(
            status_code=400,
            detail="No text found in PDF. Scanned/image-based PDFs are not supported.",
        )

    # Run analysis
    try:
        result = await analyse_resume_full(resume_text, job_description)
        return AnalysisResult(**result)
    except json.JSONDecodeError:
        raise HTTPException(
            status_code=500, detail="Failed to parse AI response. Please try again."
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")


@app.post("/api/analyse/stream")
async def analyse_stream(
    resume: UploadFile = File(...),
    job_description: str = Form(...),
):
    """Stream the AI analysis response via Server-Sent Events."""

    if not resume.filename or not resume.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported")

    contents = await resume.read()
    max_bytes = settings.max_file_size_mb * 1024 * 1024
    if len(contents) > max_bytes:
        raise HTTPException(
            status_code=400,
            detail=f"File too large. Maximum size is {settings.max_file_size_mb}MB",
        )

    if not job_description.strip():
        raise HTTPException(status_code=400, detail="Job description is required")

    try:
        resume_text = extract_text_from_pdf(contents)
    except Exception:
        raise HTTPException(status_code=400, detail="Could not parse PDF.")

    if not resume_text.strip():
        raise HTTPException(status_code=400, detail="No text found in PDF.")

    async def event_stream():
        try:
            async for chunk in analyse_resume(resume_text, job_description):
                yield f"data: {json.dumps({'type': 'chunk', 'content': chunk})}\n\n"
            yield f"data: {json.dumps({'type': 'done'})}\n\n"
        except Exception as e:
            yield f"data: {json.dumps({'type': 'error', 'content': str(e)})}\n\n"

    return StreamingResponse(
        event_stream(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
        },
    )
