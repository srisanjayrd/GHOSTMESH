from detection.engine import DetectionEngine

from edge.edge_monitor import EdgeMonitor
from edge.heartbeat import create_heartbeat


def main():

    print("\n")
    print("=" * 65)
    print("       GHOSTMESH EDGE → DETECTION TEST")
    print("=" * 65)

    # -----------------------------------------
    # LOAD DETECTION ENGINE
    # -----------------------------------------

    detection = DetectionEngine()

    detection.load_model()

    # -----------------------------------------
    # CREATE EDGE MONITOR
    # -----------------------------------------

    edge = EdgeMonitor(
        detection_engine=detection
    )

    # -----------------------------------------
    # REGISTER ESP32
    # -----------------------------------------

    print("\n[1] Registering ESP32...")

    edge.register_device(
        "ESP32-01",
        "192.168.50.10"
    )

    # -----------------------------------------
    # HEARTBEAT
    # -----------------------------------------

    print("\n[2] Sending heartbeat...")

    heartbeat = create_heartbeat(
        device_id="ESP32-01",
        ip_address="192.168.50.10"
    )

    edge.process_event(
        heartbeat
    )

    # -----------------------------------------
    # SIMULATE SECURITY EVENT
    # -----------------------------------------

    print("\n[3] Sending security event...")

    security_event = {

        "timestamp":
            heartbeat["timestamp"],

        "device_id":
            "ESP32-01",

        "source_ip":
            "192.168.50.10",

        "event_type":
            "SECURITY_EVENT",

        "connection_count":
            80,

        "unique_ports":
            25,

        "unique_destinations":
            12,

        "failed_logins":
            0,

        "bytes_sent":
            50000,

        "bytes_received":
            20000,

        "connection_rate":
            8.0
    }

    result = edge.process_event(
        security_event
    )

    # -----------------------------------------
    # FINAL RESULT
    # -----------------------------------------

    print("\n")
    print("=" * 65)
    print("              FINAL RESULT")
    print("=" * 65)

    if result:

        print(
            f"Device       : "
            f"{result['target']}"
        )

        print(
            f"Attack Type  : "
            f"{result['attack_type']}"
        )

        print(
            f"Risk Score   : "
            f"{result['risk_score']}"
        )

        print(
            f"Severity     : "
            f"{result['severity']}"
        )

        print(
            f"Action       : "
            f"{result['recommended_action']}"
        )

    print("=" * 65)


if __name__ == "__main__":
    main()