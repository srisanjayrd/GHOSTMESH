from detection.engine import DetectionEngine

from simulator.traffic_simulator import (
    normal,
    reconnaissance,
    credential_attack,
    data_access
)

from deception.deception_engine import DeceptionEngine


# =========================================================
# DISPLAY DETECTION RESULT
# =========================================================

def print_detection_result(result):

    print("\n" + "=" * 55)
    print("          GHOSTMESH DETECTION RESULT")
    print("=" * 55)

    print(f"Source IP       : {result['source_ip']}")
    print(f"Target          : {result['target']}")
    print(f"Anomaly Score   : {result['anomaly_score']}")
    print(f"Risk Score      : {result['risk_score']}")
    print(f"Trust Score     : {result['trust_score']}")
    print(f"Attack Type     : {result['attack_type']}")
    print(f"Confidence      : {result['confidence']}")
    print(f"Severity        : {result['severity']}")
    print(f"Recommended     : {result['recommended_action']}")

    if result.get("is_multi_stage"):

        print(
            "Attack Stages   : "
            + ", ".join(
                result.get("detected_stages", [])
            )
        )

    print("=" * 55)


# =========================================================
# DISPLAY DECEPTION RESULT
# =========================================================

def print_deception_result(result):

    print("\n" + "=" * 55)
    print("          GHOSTMESH DECEPTION RESULT")
    print("=" * 55)

    print(
        f"Deception Active : "
        f"{result['deception_active']}"
    )

    print(
        f"Source IP        : "
        f"{result['source_ip']}"
    )

    print(
        f"Decoy IP         : "
        f"{result['decoy_ip']}"
    )

    print(
        f"Attack Type      : "
        f"{result['attack_type']}"
    )

    print(
        f"Risk Score       : "
        f"{result['risk_score']}"
    )

    print("=" * 55)


# =========================================================
# DISPLAY FAKE DEVICES
# =========================================================

def display_fake_devices(
    deception_engine,
    source_ip
):

    print("\n[DECEPTION] Available fake resources:")

    fake_devices = deception_engine.get_fake_data(
        "devices",
        source_ip=source_ip
    )

    if isinstance(fake_devices, dict):

        if "error" in fake_devices:

            print(
                f"[!] {fake_devices['error']}"
            )

            return

    print("\nFake Devices:")

    for device in fake_devices:

        print(
            f"  - "
            f"{device['device_id']} | "
            f"{device['location']} | "
            f"{device['status']}"
        )


# =========================================================
# RECORD DECOY INTERACTION
# =========================================================

def record_demo_interaction(
    deception_engine,
    result
):

    interaction = deception_engine.record_interaction(

        source_ip=result["source_ip"],

        service="FAKE_HTTP",

        action="SUSPICIOUS_REQUEST",

        details={

            "target":
                result["target"],

            "attack_type":
                result["attack_type"],

            "risk_score":
                result["risk_score"],

            "severity":
                result["severity"]
        }
    )

    if interaction:

        print(
            "\n[+] Suspicious interaction recorded."
        )


# =========================================================
# MAIN PROGRAM
# =========================================================

def main():

    # -----------------------------------------------------
    # Initialize Detection Engine
    # -----------------------------------------------------

    print("\n[+] Initializing GHOSTMESH...")

    detection_engine = DetectionEngine()

    try:

        detection_engine.load_model()

    except FileNotFoundError:

        print("\n[ERROR] Anomaly model not found.")

        print(
            "\nPlease train the model first:"
        )

        print(
            "python train_model.py"
        )

        return

    # -----------------------------------------------------
    # Initialize Deception Engine
    # -----------------------------------------------------

    deception_engine = DeceptionEngine()

    print(
        "[+] Detection Engine ready."
    )

    print(
        "[+] Deception Engine ready."
    )

    # -----------------------------------------------------
    # Scenario mapping
    # -----------------------------------------------------

    scenarios = {

        "1": (
            "Normal traffic",
            normal
        ),

        "2": (
            "Reconnaissance",
            reconnaissance
        ),

        "3": (
            "Credential attack",
            credential_attack
        ),

        "4": (
            "Suspicious data access",
            data_access
        )
    }

    # -----------------------------------------------------
    # Simulator loop
    # -----------------------------------------------------

    while True:

        print("\n")

        print(
            "GHOSTMESH RED TEAM SIMULATOR"
        )

        print(
            "--------------------------------"
        )

        print(
            "1. Normal traffic"
        )

        print(
            "2. Reconnaissance"
        )

        print(
            "3. Credential attack"
        )

        print(
            "4. Suspicious data access"
        )

        print(
            "5. Exit"
        )

        choice = input(
            "\nSelect scenario: "
        ).strip()

        # -------------------------------------------------
        # EXIT
        # -------------------------------------------------

        if choice == "5":

            print(
                "\n[+] Stopping GHOSTMESH..."
            )

            # Stop/deactivate deception state
            if deception_engine.status().get(
                "active",
                False
            ):

                deception_engine.deactivate()

            print(
                "[+] GHOSTMESH stopped."
            )

            break

        # -------------------------------------------------
        # INVALID OPTION
        # -------------------------------------------------

        if choice not in scenarios:

            print(
                "\n[!] Invalid option."
            )

            print(
                "[!] Please select 1-5."
            )

            continue

        # -------------------------------------------------
        # SELECT SCENARIO
        # -------------------------------------------------

        scenario_name, scenario_function = (
            scenarios[choice]
        )

        print(
            f"\n[+] Running scenario: "
            f"{scenario_name}"
        )

        # -------------------------------------------------
        # Generate simulated event
        # -------------------------------------------------

        event = scenario_function()

        # -------------------------------------------------
        # MEMBER 1
        # DETECTION ENGINE
        # -------------------------------------------------

        result = detection_engine.analyze(
            event
        )

        # -------------------------------------------------
        # Display detection
        # -------------------------------------------------

        print_detection_result(
            result
        )

        # -------------------------------------------------
        # DECEPTION DECISION
        # -------------------------------------------------

        action = result[
            "recommended_action"
        ]

        # =================================================
        # CRITICAL → DECEPTION
        # =================================================

        if action == "ACTIVATE_DECEPTION":

            print(
                "\n[!] HIGH-RISK ACTIVITY DETECTED"
            )

            print(
                "[!] Activating deception environment..."
            )

            # -------------------------------------------------
            # MEMBER 2
            # DECEPTION ENGINE
            # -------------------------------------------------

            deception_result = (
                deception_engine.activate(
                    result
                )
            )

            # -------------------------------------------------
            # Display deception result
            # -------------------------------------------------

            print_deception_result(
                deception_result
            )

            # -------------------------------------------------
            # Show fake resources
            # -------------------------------------------------

            display_fake_devices(

                deception_engine,

                result["source_ip"]
            )

            # -------------------------------------------------
            # Record fake HTTP interaction
            # -------------------------------------------------

            record_demo_interaction(

                deception_engine,

                result
            )

        # =================================================
        # HIGH → ALERT
        # =================================================

        elif action == "ALERT":

            print(
                "\n[!] ALERT:"
            )

            print(
                "[!] Suspicious activity detected."
            )

            print(
                "[!] Monitoring source:"
                f" {result['source_ip']}"
            )

        # =================================================
        # MEDIUM → MONITOR
        # =================================================

        elif action == "MONITOR":

            print(
                "\n[*] Monitoring suspicious activity."
            )

        # =================================================
        # LOW → NORMAL
        # =================================================

        else:

            print(
                "\n[+] Traffic classified as normal."
            )


# =========================================================
# PROGRAM ENTRY
# =========================================================

if __name__ == "__main__":

    main()