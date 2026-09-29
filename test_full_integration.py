from detection.engine import DetectionEngine
from deception.deception_engine import DeceptionEngine

from edge.edge_monitor import EdgeMonitor
from edge.heartbeat import create_heartbeat


def create_security_event(
    device_id,
    source_ip,
    unique_ports,
    unique_destinations,
    failed_logins,
    bytes_sent,
    bytes_received,
    connection_rate
):

    return {
        "timestamp": create_heartbeat(
            device_id,
            source_ip
        )["timestamp"],

        "device_id": device_id,

        "source_ip": source_ip,

        "event_type": "SECURITY_EVENT",

        "connection_count":
            80,

        "unique_ports":
            unique_ports,

        "unique_destinations":
            unique_destinations,

        "failed_logins":
            failed_logins,

        "bytes_sent":
            bytes_sent,

        "bytes_received":
            bytes_received,

        "connection_rate":
            connection_rate
    }


def main():

    print("\n")
    print("=" * 70)
    print("       GHOSTMESH FULL EDGE SECURITY TEST")
    print("=" * 70)

    # -------------------------------------------------
    # INITIALIZE ENGINES
    # -------------------------------------------------

    print("\n[1] Initializing GHOSTMESH engines...")

    detection = DetectionEngine()

    detection.load_model()

    deception = DeceptionEngine()

    edge = EdgeMonitor(
        detection_engine=detection
    )

    print("[+] Detection Engine ready.")
    print("[+] Deception Engine ready.")
    print("[+] Edge Monitor ready.")

    # -------------------------------------------------
    # REGISTER ESP32
    # -------------------------------------------------

    print("\n[2] Registering ESP32 device...")

    device_id = "ESP32-01"
    source_ip = "192.168.50.10"

    edge.register_device(
        device_id,
        source_ip
    )

    # -------------------------------------------------
    # HEARTBEAT
    # -------------------------------------------------

    print("\n[3] ESP32 heartbeat...")

    heartbeat = create_heartbeat(
        device_id=device_id,
        ip_address=source_ip,
        temperature=27.5
    )

    edge.process_event(
        heartbeat
    )

    # -------------------------------------------------
    # STAGE 1 — RECONNAISSANCE
    # -------------------------------------------------

    print("\n")
    print("=" * 70)
    print("STAGE 1 → RECONNAISSANCE")
    print("=" * 70)

    recon_event = create_security_event(
        device_id=device_id,
        source_ip=source_ip,
        unique_ports=25,
        unique_destinations=12,
        failed_logins=0,
        bytes_sent=50000,
        bytes_received=20000,
        connection_rate=8.0
    )

    recon_result = edge.process_event(
        recon_event
    )

    print(
        f"\n[RESULT] "
        f"{recon_result['attack_type']} | "
        f"Risk: {recon_result['risk_score']} | "
        f"Action: {recon_result['recommended_action']}"
    )

    # -------------------------------------------------
    # STAGE 2 — CREDENTIAL ATTACK
    # -------------------------------------------------

    print("\n")
    print("=" * 70)
    print("STAGE 2 → CREDENTIAL ATTACK")
    print("=" * 70)

    credential_event = create_security_event(
        device_id=device_id,
        source_ip=source_ip,
        unique_ports=2,
        unique_destinations=1,
        failed_logins=30,
        bytes_sent=30000,
        bytes_received=15000,
        connection_rate=5.0
    )

    credential_result = edge.process_event(
        credential_event
    )

    print(
        f"\n[RESULT] "
        f"{credential_result['attack_type']} | "
        f"Risk: {credential_result['risk_score']} | "
        f"Action: {credential_result['recommended_action']}"
    )

    # -------------------------------------------------
    # DECEPTION DECISION
    # -------------------------------------------------

    if credential_result[
        "recommended_action"
    ] == "ACTIVATE_DECEPTION":

        print("\n")
        print("=" * 70)
        print("HIGH-RISK ATTACK DETECTED")
        print("=" * 70)

        print(
            "[!] Detection Engine recommends deception."
        )

        # ---------------------------------------------
        # ACTIVATE DECEPTION
        # ---------------------------------------------

        deception_result = deception.activate(
            credential_result
        )

        print("\n")
        print("=" * 70)
        print("DECEPTION ACTIVATED")
        print("=" * 70)

        print(
            f"Source IP  : "
            f"{deception_result['source_ip']}"
        )

        print(
            f"Attack     : "
            f"{deception_result['attack_type']}"
        )

        print(
            f"Risk Score : "
            f"{deception_result['risk_score']}"
        )

        print(
            f"Decoy IP   : "
            f"{deception_result['decoy_ip']}"
        )

        # ---------------------------------------------
        # SHOW FAKE DEVICES
        # ---------------------------------------------

        print("\n[+] Presenting synthetic IoT resources...")

        fake_devices = deception.get_fake_data(
            "devices",
            source_ip=source_ip
        )

        for device in fake_devices:

            print(
                f"  {device['device_id']} | "
                f"{device['location']} | "
                f"{device['status']}"
            )

        # ---------------------------------------------
        # RECORD INTERACTION
        # ---------------------------------------------

        print(
            "\n[+] Recording suspicious interaction..."
        )

        deception.record_interaction(

            source_ip=source_ip,

            service="GHOSTMESH-DECOY",

            action="MULTI_STAGE_ATTACK_CAPTURED",

            details={
                "device_id": device_id,
                "attack_type":
                    credential_result[
                        "attack_type"
                    ],
                "risk_score":
                    credential_result[
                        "risk_score"
                    ]
            }
        )

    else:

        print(
            "\n[!] Deception was not activated."
        )

    # -------------------------------------------------
    # FINAL STATUS
    # -------------------------------------------------

    print("\n")
    print("=" * 70)
    print("             FINAL GHOSTMESH STATUS")
    print("=" * 70)

    print(
        f"Device       : {device_id}"
    )

    print(
        f"Source IP    : {source_ip}"
    )

    print(
        f"Attack       : "
        f"{credential_result['attack_type']}"
    )

    print(
        f"Risk Score   : "
        f"{credential_result['risk_score']}"
    )

    print(
        f"Severity     : "
        f"{credential_result['severity']}"
    )

    print(
        f"Action       : "
        f"{credential_result['recommended_action']}"
    )

    print(
        f"Deception    : "
        f"{deception.status()['active']}"
    )

    print("=" * 70)

    print(
        "\n[+] FULL EDGE → DETECTION → DECEPTION "
        "TEST COMPLETED."
    )


if __name__ == "__main__":
    main()