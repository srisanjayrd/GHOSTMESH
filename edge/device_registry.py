from datetime import datetime


class DeviceRegistry:

    def __init__(self):

        self.devices = {}

    def register_device(
        self,
        device_id,
        ip_address,
        device_type="ESP32"
    ):

        if device_id not in self.devices:

            self.devices[device_id] = {
                "device_id": device_id,
                "ip_address": ip_address,
                "device_type": device_type,
                "status": "OFFLINE",
                "last_heartbeat": None,
                "trust_score": 100
            }

            print(
                f"[EDGE] Device registered: "
                f"{device_id}"
            )

    def update_heartbeat(self, device_id):

        if device_id not in self.devices:

            print(
                f"[EDGE] Unknown device: "
                f"{device_id}"
            )

            return False

        self.devices[device_id][
            "status"
        ] = "ONLINE"

        self.devices[device_id][
            "last_heartbeat"
        ] = datetime.now().isoformat()

        print(
            f"[EDGE] Heartbeat received: "
            f"{device_id}"
        )

        return True

    def update_trust(
        self,
        device_id,
        trust_score
    ):

        if device_id not in self.devices:
            return False

        self.devices[device_id][
            "trust_score"
        ] = max(
            0,
            min(100, trust_score)
        )

        return True

    def mark_offline(self, device_id):

        if device_id not in self.devices:
            return False

        self.devices[device_id][
            "status"
        ] = "OFFLINE"

        return True

    def get_device(self, device_id):

        return self.devices.get(
            device_id
        )

    def get_all_devices(self):

        return list(
            self.devices.values()
        )

    def print_devices(self):

        print("\n" + "=" * 60)
        print("             GHOSTMESH DEVICE REGISTRY")
        print("=" * 60)

        if not self.devices:

            print("No devices registered.")

        for device in self.devices.values():

            print(
                f"Device ID    : "
                f"{device['device_id']}"
            )

            print(
                f"IP Address   : "
                f"{device['ip_address']}"
            )

            print(
                f"Type         : "
                f"{device['device_type']}"
            )

            print(
                f"Status       : "
                f"{device['status']}"
            )

            print(
                f"Trust Score  : "
                f"{device['trust_score']}"
            )

            print(
                f"Last Heartbeat: "
                f"{device['last_heartbeat']}"
            )

            print("-" * 60)