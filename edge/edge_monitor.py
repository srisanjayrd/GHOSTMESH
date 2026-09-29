from edge.device_registry import DeviceRegistry


class EdgeMonitor:

    def __init__(self, detection_engine=None):

        self.registry = DeviceRegistry()
        self.detection_engine = detection_engine

    def register_device(
        self,
        device_id,
        ip_address,
        device_type="ESP32"
    ):

        self.registry.register_device(
            device_id,
            ip_address,
            device_type
        )

    def process_event(self, event):

        device_id = event.get("device_id")
        event_type = event.get("event_type")

        if event_type == "HEARTBEAT":

            success = self.registry.update_heartbeat(
                device_id
            )

            if success:

                print(
                    f"[EDGE] {device_id} is ONLINE"
                )

        elif event_type == "DEVICE_OFFLINE":

            self.registry.mark_offline(
                device_id
            )

            print(
                f"[EDGE] {device_id} is OFFLINE"
            )

        elif event_type == "SECURITY_EVENT":

            print(
                f"[EDGE] Security event received "
                f"from {device_id}"
            )

            if self.detection_engine:

                detection_event = {
                    "timestamp": event.get("timestamp"),
                    "source_ip": event.get(
                        "source_ip",
                        "unknown"
                    ),
                    "target": device_id,

                    "connection_count": event.get(
                        "connection_count",
                        0
                    ),

                    "unique_ports": event.get(
                        "unique_ports",
                        0
                    ),

                    "unique_destinations": event.get(
                        "unique_destinations",
                        0
                    ),

                    "failed_logins": event.get(
                        "failed_logins",
                        0
                    ),

                    "bytes_sent": event.get(
                        "bytes_sent",
                        0
                    ),

                    "bytes_received": event.get(
                        "bytes_received",
                        0
                    ),

                    "connection_rate": event.get(
                        "connection_rate",
                        0
                    )
                }

                result = (
                    self.detection_engine.analyze(
                        detection_event
                    )
                )

                print(
                    "\n[EDGE → DETECTION]"
                )

                print(
                    f"Attack Type : "
                    f"{result['attack_type']}"
                )

                print(
                    f"Risk Score  : "
                    f"{result['risk_score']}"
                )

                print(
                    f"Severity    : "
                    f"{result['severity']}"
                )

                print(
                    f"Action      : "
                    f"{result['recommended_action']}"
                )

                return result

        else:

            print(
                f"[EDGE] Unknown event: "
                f"{event_type}"
            )

        return None

    def get_devices(self):

        return self.registry.get_all_devices()

    def show_status(self):

        self.registry.print_devices()