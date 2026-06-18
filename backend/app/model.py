import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline
import joblib
import json

MODEL_PATH = os.path.join(os.path.dirname(__file__), '..', 'model.joblib')
METRICS_PATH = os.path.join(os.path.dirname(__file__), '..', 'metrics.json')


def build_pipeline():
    pipe = Pipeline([
        ('tfidf', TfidfVectorizer(stop_words='english', max_features=5000)),
        ('rf', RandomForestClassifier(n_estimators=200, random_state=42))
    ])
    return pipe


def save_pipeline(pipe):
    joblib.dump(pipe, MODEL_PATH)


def load_pipeline():
    if os.path.exists(MODEL_PATH):
        return joblib.load(MODEL_PATH)
    return None


def save_metrics(metrics: dict):
    with open(METRICS_PATH, 'w', encoding='utf-8') as f:
        json.dump(metrics, f, indent=2)


def load_metrics():
    if os.path.exists(METRICS_PATH):
        with open(METRICS_PATH, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}
