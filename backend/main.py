# main.py

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from predictor import analyze_text

app = FastAPI(title="TruthMark API", version="1.0")

# --------------------
# CORS
# --------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --------------------
# Request Schema
# --------------------
class TextRequest(BaseModel):
    text: str = Field(
        ...,
        min_length=10,
        description="Text to analyze (50–350 words recommended)"
    )

# --------------------
# Response Schema
# --------------------
class AnalyzeResponse(BaseModel):
    overall_ai_score: float
    overall_human_score: float
    verdict: str
    confidence: str
    badge_color: str
    breakdown: dict
    model_note: str
    limitations: list

# --------------------
# Utils
# --------------------
def count_words(text: str):
    return len(text.strip().split())

# --------------------
# Endpoint
# --------------------
@app.post("/analyze-text", response_model=AnalyzeResponse)
async def analyze(req: TextRequest):
    text = req.text.strip()
    wc = count_words(text)

    if wc < 50:
        raise HTTPException(
            status_code=400,
            detail="Minimum 50 words required for reliable analysis."
        )

    if wc > 350:
        raise HTTPException(
            status_code=400,
            detail="Maximum 350 words allowed. Please shorten the text."
        )

    return analyze_text(text)
