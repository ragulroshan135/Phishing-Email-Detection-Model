import re
from urllib.parse import urlparse
import ipaddress
import datetime

SHORTENER_DOMAINS = set([
    "bit.ly","tinyurl.com","t.co","ow.ly","buff.ly","goo.gl","is.gd"
])

KEYWORDS = [
    "urgent","verify","password","login","account suspended","reward","bank","click here","verify your",
]

URL_REGEX = re.compile(r"https?://[\w\-\.\:/%\?=&]+|www\.[\w\-\.\:/%\?=&]+")


def extract_urls(text):
    return URL_REGEX.findall(text or "")


def analyze_url(url):
    findings = []
    try:
        parsed = urlparse(url)
        hostname = parsed.hostname or ""
        if hostname and any(short in hostname for short in SHORTENER_DOMAINS):
            findings.append("url_shortener")
        # IP-based URL
        try:
            ipaddress.ip_address(hostname)
            findings.append("ip_in_url")
        except Exception:
            pass
        # Non-standard TLD
        parts = hostname.split('.')
        if len(parts) > 1:
            tld = parts[-1]
            if len(tld) > 3:  # simple heuristic for non-standard tld
                findings.append("non_standard_tld")
        # suspicious patterns
        if parsed.path and len(parsed.path) > 40:
            findings.append("long_path")
    except Exception:
        findings.append("parse_error")
    return findings


def detect_keywords(text):
    text_low = (text or "").lower()
    found = []
    for kw in KEYWORDS:
        if kw in text_low:
            found.append(kw)
    return found


def threat_score_from_indicators(indicators):
    # indicators: dict with counts
    score = 0
    # base weights
    score += indicators.get('num_suspicious_urls', 0) * 25
    score += min(indicators.get('num_keywords', 0), 4) * 10
    score += indicators.get('url_flags', 0) * 15
    # clamp
    score = max(0, min(100, score))
    return int(score)


def now_iso():
    return datetime.datetime.utcnow().isoformat() + 'Z'
