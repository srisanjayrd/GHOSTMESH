import pandas as pd

from detection.anomaly import AnomalyDetector


DATA_PATH = "data/normal_traffic.csv"


def main():

    print("=" * 50)
    print("GHOSTMESH - TRAINING ANOMALY DETECTOR")
    print("=" * 50)

    data = pd.read_csv(DATA_PATH)

    print("\nNormal samples:")
    print(len(data))

    detector = AnomalyDetector()

    detector.train(data)

    print("\n[+] Training completed")
    print("[+] Model saved")


if __name__ == "__main__":
    main()