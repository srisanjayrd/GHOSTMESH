import json
import socketserver
import threading

from deception.fake_database import FakeDatabase
from deception.interaction_logger import InteractionLogger

HOST = "127.0.0.1"
PORT = 5432

database = FakeDatabase()
logger = InteractionLogger()


class DatabaseHandler(socketserver.StreamRequestHandler):

    def handle(self):
        source_ip = self.client_address[0]

        logger.log(
            source_ip,
            "FAKE_DATABASE",
            "CONNECTED"
        )

        self.wfile.write(
            b"GHOSTMESH SYNTHETIC DATABASE\n"
            b"Available commands: DEVICES, USERS, SYSTEM, EXIT\n"
        )

        try:
            while True:
                line = self.rfile.readline(256)

                if not line:
                    break

                command = line.decode(
                    "utf-8", errors="replace"
                ).strip().upper()

                if command == "EXIT":
                    break

                tables = {
                    "DEVICES": "devices",
                    "USERS": "users",
                    "SYSTEM": "system"
                }

                if command in tables:
                    result = database.query(
                        tables[command]
                    )
                else:
                    result = {
                        "error": "UNKNOWN_COMMAND"
                    }

                logger.log(
                    source_ip,
                    "FAKE_DATABASE",
                    "COMMAND",
                    {"command": command[:50]}
                )

                response = json.dumps(result) + "\n"

                self.wfile.write(
                    response.encode("utf-8")
                )

        finally:
            logger.log(
                source_ip,
                "FAKE_DATABASE",
                "DISCONNECTED"
            )


class DatabaseServer(
    socketserver.ThreadingMixIn,
    socketserver.TCPServer
):
    allow_reuse_address = True
    daemon_threads = True


def start_fake_db():
    with DatabaseServer(
        (HOST, PORT),
        DatabaseHandler
    ) as server:

        print(
            f"[+] Fake Database running "
            f"on {HOST}:{PORT}"
        )

        server.serve_forever()


def start_fake_db_background():
    thread = threading.Thread(
        target=start_fake_db,
        daemon=True
    )

    thread.start()
    return thread


if __name__ == "__main__":
    start_fake_db()