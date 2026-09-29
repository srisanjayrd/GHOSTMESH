import os
import joblib
import numpy as np
from sklearn.ensemble import IsolationForest

from detection.features import FEATURE_COLUMNS


class AnomalyDetector:

    def __init__(self, model_path="models/anomaly_model.pkl"):
        self.model_path = model_path
        self.model = None

    def train(self, normal_data):

        self.model = IsolationForest(
            n_estimators=150,
            contamination=0.05,
            random_state=42
        )

        self.model.fit(normal_data[FEATURE_COLUMNS])

        os.makedirs(
            os.path.dirname(self.model_path),
            exist_ok=True
        )

        joblib.dump(self.model, self.model_path)

        print("[+] Anomaly model trained")

    def load(self):

        if not os.path.exists(self.model_path):
            raise FileNotFoundError(
                "Anomaly model not found. Train the model first."
            )

        self.model = joblib.load(self.model_path)

        print("[+] Anomaly model loaded")

    def predict(self, features):

        if self.model is None:
            raise RuntimeError("Model is not loaded.")

        prediction = self.model.predict(
            features[FEATURE_COLUMNS]
        )[0]

        raw_score = self.model.decision_function(
            features[FEATURE_COLUMNS]
        )[0]

        # Convert Isolation Forest score into approximately 0-1
        anomaly_score = 1 / (1 + np.exp(5 * raw_score))

        is_anomaly = prediction == -1

        return {
            "is_anomaly": bool(is_anomaly),
            "anomaly_score": round(
                float(anomaly_score), 3
            )
        }