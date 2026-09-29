import json
import os
import threading
from datetime import datetime


class InteractionLogger:

    def __init__(self, log_file="logs/deception_events.json"):

        self.log_file = log_file

        os.makedirs(
            os.path.dirname(self.log_file),
            exist_ok=True
        )

        self.lock = threading.Lock()

        if not os.path.exists(self.log_file):

            with open(
                self.log_file,
                "w",
                encoding="utf-8"
            ) as f:

                json.dump([], f, indent=4)

    def log(
        self,
        source_ip,
        service,
        action,
        details=None
    ):

        event = {
            "timestamp": datetime.now().isoformat(),
            "source_ip": source_ip,
            "service": service,
            "action": action,
            "details": details or {}
        }

        # Prevent multiple decoy threads from
        # reading/writing the JSON file at the same time.
        with self.lock:

            try:

                with open(
                    self.log_file,
                    "r",
                    encoding="utf-8"
                ) as f:

                    events = json.load(f)

                    if not isinstance(events, list):
                        events = []

            except (
                json.JSONDecodeError,
                FileNotFoundError
            ):

                events = []

            events.append(event)

            # Write through a temporary file first
            # so the main log doesn't become empty/corrupt.
            temp_file = self.log_file + ".tmp"

            with open(
                temp_file,
                "w",
                encoding="utf-8"
            ) as f:

                json.dump(
                    events,
                    f,
                    indent=4
                )

            os.replace(
                temp_file,
                self.log_file
            )

        print(
            f"[DECEPTION] {service} | "
            f"{action} | {source_ip}"
        )

        return event