from deception.config import (
    DECOY_NAME,
    DECOY_IP,
    FAKE_SERVICES
)


class DecoyManager:

    def __init__(self):

        self.active = False

        self.services = {
            service: {
                "port": port,
                "status": "OFFLINE"
            }

            for service, port in FAKE_SERVICES.items()
        }

    def activate(self):

        self.active = True

        for service in self.services:
            self.services[service]["status"] = "ONLINE"

        print("\n[+] DECEPTION ENVIRONMENT ACTIVATED")
        print(f"[+] Decoy: {DECOY_NAME}")
        print(f"[+] IP: {DECOY_IP}")

        for service, info in self.services.items():

            print(
                f"[+] {service} "
                f"→ port {info['port']} "
                f"[ONLINE]"
            )

    def deactivate(self):

        self.active = False

        for service in self.services:
            self.services[service]["status"] = "OFFLINE"

        print("\n[-] Deception environment deactivated")

    def status(self):

        return {
            "active": self.active,
            "decoy": DECOY_NAME,
            "ip": DECOY_IP,
            "services": self.services
        }