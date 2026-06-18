import io
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet


def generate_pdf_report(analysis: dict) -> bytes:
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()
    flow = []

    title = Paragraph('Phishing Threat Analysis Report', styles['Title'])
    flow.append(title)
    flow.append(Spacer(1, 12))

    meta = (
        f"Prediction: {analysis.get('prediction')} | Confidence: {analysis.get('confidence')}% | Threat Score: {analysis.get('threat_score')}"
    )
    flow.append(Paragraph(meta, styles['Normal']))
    flow.append(Spacer(1, 12))

    flow.append(Paragraph('Indicators', styles['Heading2']))
    flow.append(Spacer(1, 6))

    # Keywords
    keywords = analysis.get('indicators', {}).get('keywords', [])
    urls = analysis.get('indicators', {}).get('urls', [])

    if keywords:
        flow.append(Paragraph('Keywords detected:', styles['Normal']))
        for k in keywords:
            flow.append(Paragraph(f'- {k}', styles['Bullet']))
    else:
        flow.append(Paragraph('No suspicious keywords detected.', styles['Normal']))

    flow.append(Spacer(1, 8))
    flow.append(Paragraph('URLs detected:', styles['Normal']))
    if urls:
        data = [['URL', 'Flags']]
        for u in urls:
            data.append([u.get('url', ''), ', '.join(u.get('flags', []))])
        t = Table(data, colWidths=[330, 180])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
        ]))
        flow.append(t)
    else:
        flow.append(Paragraph('No URLs detected.', styles['Normal']))

    flow.append(Spacer(1, 12))
    flow.append(Paragraph('Recommendations', styles['Heading2']))
    recs = [
        'Do not click suspicious links',
        'Verify sender identity',
        'Avoid sharing credentials',
        'Report the email to your security team'
    ]
    for r in recs:
        flow.append(Paragraph(f'- {r}', styles['Bullet']))

    flow.append(Spacer(1, 12))
    flow.append(Paragraph(f"Analysis timestamp: {analysis.get('timestamp')}", styles['Normal']))

    doc.build(flow)
    buffer.seek(0)
    return buffer.read()
