import io
from fastapi import FastAPI, HTTPException, Response
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from app.model import load_pipeline, load_metrics
from app.utils import extract_urls, analyze_url, detect_keywords, threat_score_from_indicators, now_iso
from app.report import generate_pdf_report
import uvicorn

app = FastAPI(title='Phishing Email Detection Model')

class AnalyzeRequest(BaseModel):
    email: str


@app.on_event('startup')
async def startup_event():
    global PIPE, METRICS
    PIPE = load_pipeline()
    METRICS = load_metrics()


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

    # prediction
    if PIPE is None:
        prediction = 'unknown'
        confidence = 0.0
    else:
        prob = float(PIPE.predict_proba([text])[:, 1][0])
        pred = int(PIPE.predict([text])[0])
        prediction = 'phishing' if pred == 1 else 'safe'
        confidence = round(prob * 100, 2)

    explain = []
    if len(urls) > 0:
        explain.append('Suspicious URL detected')
    if any(k for k in keywords if 'password' in k or 'verify' in k or 'login' in k):
        explain.append('Urgency or credential request language found')
    if threat_score > 80:
        explain.append('High threat score')

    resp = {
        'prediction': prediction,
        'confidence': confidence,
        'threat_score': threat_score,
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
    return METRICS or {}


if __name__ == '__main__':
    uvicorn.run('app.main:app', host='0.0.0.0', port=8000, reload=True)
