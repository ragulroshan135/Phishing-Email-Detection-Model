from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from app.utils import extract_urls, analyze_url, detect_keywords, threat_score_from_indicators, now_iso
from app.report import generate_pdf_report
from fastapi.responses import StreamingResponse
import io

app = FastAPI(title='Phishing Email Detection Model (Mock)')

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class AnalyzeRequest(BaseModel):
    email: str


def analyze_text(text: str) -> dict:
    text = text or ''
    if not text.strip():
        raise ValueError('Email text is required')
    urls = extract_urls(text)
    url_flags = 0
    url_details = []
    for u in urls:
        flags = analyze_url(u)
        url_flags += len(flags)
        url_details.append({'url': u, 'flags': flags})

    keywords = detect_keywords(text)

    indicators = {
        'num_suspicious_urls': len(urls),
        'num_keywords': len(keywords),
        'url_flags': url_flags,
    }

    threat_score = threat_score_from_indicators(indicators)

    # Simple rule-based prediction for mock server
    if threat_score >= 60 or indicators['num_suspicious_urls'] > 0 or indicators['num_keywords'] >= 2:
        prediction = 'phishing'
        confidence = min(99.9, threat_score + 10)
    else:
        prediction = 'safe'
        confidence = max(10.0, 100 - threat_score)

    explain = []
    if len(urls) > 0:
        explain.append('Suspicious URL detected')
    if any(k for k in keywords if 'password' in k or 'verify' in k or 'login' in k):
        explain.append('Urgency or credential request language found')
    if threat_score > 80:
        explain.append('High threat score')

    resp = {
        'prediction': prediction,
        'confidence': round(float(confidence), 2),
        'threat_score': int(threat_score),
        'indicators': {
            'urls': url_details,
            'keywords': keywords,
        },
        'explanation': explain,
        'timestamp': now_iso()
    }
    return resp


@app.post('/analyze')
async def analyze(req: AnalyzeRequest):
    try:
        return analyze_text(req.email)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post('/report')
async def report(req: AnalyzeRequest):
    try:
        analysis = analyze_text(req.email)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    pdf_bytes = generate_pdf_report(analysis)
    return StreamingResponse(io.BytesIO(pdf_bytes), media_type='application/pdf')


@app.get('/metrics')
async def metrics():
    # Return a small mock metrics object so frontend can display them
    return {
        'accuracy': 0.92,
        'precision': 0.9,
        'recall': 0.88,
        'f1': 0.89,
        'confusion_matrix': [[50, 5], [6, 39]]
    }
