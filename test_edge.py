from edge.edge_monitor import EdgeMonitor
from edge.heartbeat import (
    create_heartbeat,
    create_offline_event
)


def main():

    print("\n")
    print("=" * 60)
    print("       GHOSTMESH EDGE SECURITY TEST")
    print("=" * 60)

    edge = EdgeMonitor()

    # ---------------------------------------------
    # REGISTER ESP32 DEVICES
    # ---------------------------------------------

    print("\n[1] Registering ESP32 devices...")

    edge.register_device(
        "ESP32-01",
        "192.168.50.10"
    )

    edge.register_device(
        "ESP32-02",
        "192.168.50.11"
    )

    # ---------------------------------------------
    # HEARTBEAT FROM ESP32-01
    # ---------------------------------------------

    print("\n[2] ESP32-01 heartbeat...")

    heartbeat = create_heartbeat(
        device_id="ESP32-01",
        ip_address="192.168.50.10",
        temperature=27.5
    )

    edge.process_event(
        heartbeat
    )

    # ---------------------------------------------
    # HEARTBEAT FROM ESP32-02
    # ---------------------------------------------

    print("\n[3] ESP32-02 heartbeat...")

    heartbeat = create_heartbeat(
        device_id="ESP32-02",
        ip_address="192.168.50.11",
        temperature=28.1
    )

    edge.process_event(
        heartbeat
    )

    # ---------------------------------------------
    # DISPLAY STATUS
    # ---------------------------------------------

    print("\n[4] Current device status...")

    edge.show_status()

    # ---------------------------------------------
    # SIMULATE ESP32-02 OFFLINE
    # ---------------------------------------------

    print("\n[5] Simulating ESP32-02 offline...")

    offline_event = create_offline_event(
        device_id="ESP32-02",
        ip_address="192.168.50.11"
    )

    edge.process_event(
        offline_event
    )

    # ---------------------------------------------
    # DISPLAY FINAL STATUS
    # ---------------------------------------------

    print("\n[6] Final device status...")

    edge.show_status()

    print("\n" + "=" * 60)
    print("       EDGE SECURITY TEST COMPLETED")
    print("=" * 60)


if __name__ == "__main__":
    main()