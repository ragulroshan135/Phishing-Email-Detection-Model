import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
from app.model import build_pipeline, save_pipeline, save_metrics
import os

DATA_PATH = os.path.join(os.path.dirname(__file__), 'data', 'sample_emails.csv')


def load_data():
    df = pd.read_csv(DATA_PATH)
    df = df.dropna()
    df['label_bin'] = df['label'].apply(lambda x: 1 if x.strip().lower() == 'phishing' else 0)
    return df['text'].tolist(), df['label_bin'].tolist()


def main():
    X, y = load_data()
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42, stratify=y)
    pipe = build_pipeline()
    pipe.fit(X_train, y_train)
    preds = pipe.predict(X_test)
    probs = pipe.predict_proba(X_test)[:, 1]

    metrics = {
        'accuracy': float(accuracy_score(y_test, preds)),
        'precision': float(precision_score(y_test, preds, zero_division=0)),
        'recall': float(recall_score(y_test, preds, zero_division=0)),
        'f1': float(f1_score(y_test, preds, zero_division=0)),
        'confusion_matrix': confusion_matrix(y_test, preds).tolist()
    }
    save_pipeline(pipe)
    save_metrics(metrics)
    print('Training complete. Metrics:')
    print(metrics)


if __name__ == '__main__':
    main()
