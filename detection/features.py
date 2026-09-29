import pandas as pd


FEATURE_COLUMNS = [
    "connection_count",
    "unique_ports",
    "unique_destinations",
    "failed_logins",
    "bytes_sent",
    "bytes_received",
    "connection_rate"
]


def extract_features(event: dict) -> pd.DataFrame:
    """
    Convert one network behaviour event into an ML feature vector.
    """

    features = {
        "connection_count": event.get("connection_count", 0),
        "unique_ports": event.get("unique_ports", 0),
        "unique_destinations": event.get("unique_destinations", 0),
        "failed_logins": event.get("failed_logins", 0),
        "bytes_sent": event.get("bytes_sent", 0),
        "bytes_received": event.get("bytes_received", 0),
        "connection_rate": event.get("connection_rate", 0.0)
    }

    return pd.DataFrame([features], columns=FEATURE_COLUMNS)