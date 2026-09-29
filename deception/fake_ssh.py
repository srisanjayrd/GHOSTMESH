import socket
import threading
from datetime import datetime
import json
import os


HOST = "127.0.0.1"
PORT = 2222

LOG_FILE = "logs/deception_events.json"


# =========================================================
# LOGGING
# =========================================================

def save_event(event):

    os.makedirs("logs", exist_ok=True)

    if os.path.exists(LOG_FILE):

        try:
            with open(LOG_FILE, "r") as f:
                events = json.load(f)

        except (json.JSONDecodeError, FileNotFoundError):

            events = []

    else:

        events = []

    events.append(event)

    with open(LOG_FILE, "w") as f:

        json.dump(
            events,
            f,
            indent=4
        )


def log_interaction(
    source_ip,
    action,
    details=None
):

    event = {

        "timestamp":
            datetime.now().isoformat(),

        "source_ip":
            source_ip,

        "service":
            "FAKE_SSH",

        "action":
            action,

        "details":
            details or {}
    }

    print(
        f"[DECEPTION] SSH | "
        f"{action} | "
        f"{source_ip}"
    )

    save_event(event)


# =========================================================
# CLIENT HANDLER
# =========================================================

def handle_client(
    client_socket,
    client_address
):

    source_ip = client_address[0]

    try:

        # ---------------------------------------------
        # Log connection
        # ---------------------------------------------

        log_interaction(
            source_ip,
            "CONNECTION"
        )

        # ---------------------------------------------
        # Synthetic SSH-like banner
        # ---------------------------------------------

        banner = (
            b"SSH-2.0-GHOSTMESH-DECOY\r\n"
        )

        client_socket.sendall(
            banner
        )

        # ---------------------------------------------
        # Receive a small amount of data
        # ---------------------------------------------

        client_socket.settimeout(5)

        try:

            data = client_socket.recv(1024)

        except socket.timeout:

            data = b""

        # ---------------------------------------------
        # Record only metadata
        # ---------------------------------------------

        if data:

            log_interaction(

                source_ip,

                "CLIENT_RESPONSE",

                {
                    "bytes_received":
                        len(data)
                }
            )

        else:

            log_interaction(
                source_ip,
                "NO_RESPONSE"
            )

        # ---------------------------------------------
        # Send safe synthetic response
        # ---------------------------------------------

        response = (
            b"GHOSTMESH DECOY SERVICE\r\n"
            b"Demo environment only.\r\n"
            b"Connection recorded.\r\n"
        )

        client_socket.sendall(
            response
        )

    except Exception as error:

        log_interaction(

            source_ip,

            "CONNECTION_ERROR",

            {
                "error":
                    str(error)
            }
        )

    finally:

        client_socket.close()

        log_interaction(
            source_ip,
            "DISCONNECTED"
        )


# =========================================================
# START SERVER
# =========================================================

def start_fake_ssh():

    server = socket.socket(
        socket.AF_INET,
        socket.SOCK_STREAM
    )

    server.setsockopt(
        socket.SOL_SOCKET,
        socket.SO_REUSEADDR,
        1
    )

    server.bind(
        (HOST, PORT)
    )

    server.listen(5)

    print("\n" + "=" * 55)
    print("       GHOSTMESH FAKE SSH DECOY")
    print("=" * 55)

    print(
        f"[+] Server running on "
        f"{HOST}:{PORT}"
    )

    print(
        "[+] Synthetic SSH-like service"
    )

    print(
        "[+] No real authentication is performed."
    )

    print(
        "[+] Press CTRL+C to stop.\n"
    )

    try:

        while True:

            client_socket, client_address = (
                server.accept()
            )

            thread = threading.Thread(

                target=handle_client,

                args=(
                    client_socket,
                    client_address
                ),

                daemon=True
            )

            thread.start()

    except KeyboardInterrupt:

        print(
            "\n[-] Fake SSH server stopped."
        )

    finally:

        server.close()


# =========================================================
# BACKGROUND START
# =========================================================

def start_fake_ssh_background():

    thread = threading.Thread(

        target=start_fake_ssh,

        daemon=True
    )

    thread.start()

    return thread


# =========================================================
# MAIN
# =========================================================

if __name__ == "__main__":

    start_fake_ssh()