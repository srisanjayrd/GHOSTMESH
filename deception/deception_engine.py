from deception.decoy_manager import DecoyManager
from deception.interaction_logger import InteractionLogger
from deception.fake_database import FakeDatabase

from deception.fake_http import start_fake_http_background
from deception.fake_ssh import start_fake_ssh_background
from deception.fake_db_server import start_fake_db_background

class DeceptionEngine:

    def __init__(self):

        self.decoy_manager = DecoyManager()
        self.logger = InteractionLogger()
        self.database = FakeDatabase()

        self.activation_count = 0

        # Track decoy service threads
        self.http_thread = None
        self.ssh_thread = None
        self.db_thread = None

    def activate(self, detection_result):

        source_ip = detection_result.get(
            "source_ip",
            "unknown"
        )

        attack_type = detection_result.get(
            "attack_type",
            "UNKNOWN"
        )

        risk_score = detection_result.get(
            "risk_score",
            0
        )

        print("\n" + "=" * 55)
        print("       GHOSTMESH DECEPTION ENGINE")
        print("=" * 55)

        print(f"Source IP    : {source_ip}")
        print(f"Attack Type  : {attack_type}")
        print(f"Risk Score   : {risk_score}")

        # Activate decoy manager
        self.decoy_manager.activate()

        self.activation_count += 1

        # ------------------------------------------------
        # START FAKE HTTP
        # ------------------------------------------------

        if self.http_thread is None:

            print("\n[+] Starting Fake HTTP Decoy...")

            self.http_thread = (
                start_fake_http_background()
            )

            print("[+] Fake HTTP Decoy started.")

        # ------------------------------------------------
        # START FAKE SSH
        # ------------------------------------------------

        if self.ssh_thread is None:

            print("\n[+] Starting Fake SSH Decoy...")

            self.ssh_thread = (
                start_fake_ssh_background()
            )

            print("[+] Fake SSH Decoy started.")
        if self.db_thread is None:
            print("\n[+] Starting Fake Database Decoy...")
            self.db_thread = (
                start_fake_db_background()
                )
            print("[+] Fake Database Decoy started.")

        # ------------------------------------------------
        # LOG DECEPTION ACTIVATION
        # ------------------------------------------------

        self.logger.log(
            source_ip=source_ip,
            service="DECEPTION_ENGINE",
            action="ACTIVATED",
            details={
                "attack_type": attack_type,
                "risk_score": risk_score,
                "activation_number": self.activation_count
            }
        )

        return {
            "deception_active": True,
            "source_ip": source_ip,
            "decoy_ip": "192.168.50.100",
            "attack_type": attack_type,
            "risk_score": risk_score
        }

    # ----------------------------------------------------
    # RECORD INTERACTION
    # ----------------------------------------------------

    def record_interaction(
        self,
        source_ip,
        service,
        action,
        details=None
    ):

        if not self.decoy_manager.active:

            print(
                "[!] Deception environment "
                "is not active."
            )

            return None

        return self.logger.log(
            source_ip,
            service,
            action,
            details
        )

    # ----------------------------------------------------
    # FAKE DATABASE
    # ----------------------------------------------------

    def get_fake_data(
        self,
        table,
        source_ip="unknown"
    ):

        if not self.decoy_manager.active:

            return {
                "error": "DECEPTION_INACTIVE"
            }

        result = self.database.query(table)

        self.logger.log(
            source_ip=source_ip,
            service="FAKE_DATABASE",
            action="DATA_ACCESS",
            details={
                "table": table
            }
        )

        return result

    # ----------------------------------------------------
    # STATUS
    # ----------------------------------------------------

    def status(self):

        return self.decoy_manager.status()

    # ----------------------------------------------------
    # DEACTIVATE
    # ----------------------------------------------------

    def deactivate(self):

        self.decoy_manager.deactivate()

        return {
            "deception_active": False
        }