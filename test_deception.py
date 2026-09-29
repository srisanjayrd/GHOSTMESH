from deception.deception_engine import DeceptionEngine


def main():

    print("\n")
    print("=" * 60)
    print("       GHOSTMESH DECEPTION ENGINE TEST")
    print("=" * 60)

    # Create deception engine
    engine = DeceptionEngine()

    # -------------------------------------------------
    # Fake detection result from Member 1
    # -------------------------------------------------

    detection_result = {
        "source_ip": "192.168.50.10",
        "target": "ESP32-01",
        "attack_type": "MULTI_STAGE_ATTACK",
        "risk_score": 0.95,
        "trust_score": 73.28,
        "severity": "CRITICAL",
        "confidence": 0.86,
        "recommended_action": "ACTIVATE_DECEPTION"
    }

    # -------------------------------------------------
    # Activate deception
    # -------------------------------------------------

    print("\n[1] Activating deception...")

    result = engine.activate(
        detection_result
    )

    print("\nDECEPTION RESULT")
    print("-" * 40)

    for key, value in result.items():
        print(f"{key}: {value}")

    # -------------------------------------------------
    # Test fake database
    # -------------------------------------------------

    print("\n[2] Testing fake database...")

    devices = engine.get_fake_data(
        "devices"
    )

    print("\nFake Devices:")

    for device in devices:

        print(
            f"  Device ID : {device['device_id']}"
        )

        print(
            f"  Location  : {device['location']}"
        )

        print(
            f"  Status    : {device['status']}"
        )

        print()

    # -------------------------------------------------
    # Test fake users
    # -------------------------------------------------

    print("[3] Testing fake users...")

    users = engine.get_fake_data(
        "users"
    )

    print("\nFake Users:")

    for user in users:

        print(
            f"  Username : {user['username']}"
        )

        print(
            f"  Role     : {user['role']}"
        )

        print()

    # -------------------------------------------------
    # Simulate suspicious interaction
    # -------------------------------------------------

    print("[4] Recording suspicious interaction...")

    interaction = engine.record_interaction(

        source_ip="192.168.50.10",

        service="FAKE_HTTP",

        action="SUSPICIOUS_REQUEST",

        details={
            "page": "/admin",
            "method": "GET",
            "attack_type": "MULTI_STAGE_ATTACK"
        }
    )

    print("\nInteraction recorded:")

    print(interaction)

    # -------------------------------------------------
    # Check deception status
    # -------------------------------------------------

    print("\n[5] Checking deception status...")

    status = engine.status()

    print(status)

    # -------------------------------------------------
    # Finish
    # -------------------------------------------------

    print("\n" + "=" * 60)
    print("       DECEPTION ENGINE TEST COMPLETED")
    print("=" * 60)


if __name__ == "__main__":
    main()