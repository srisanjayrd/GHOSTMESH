from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse
from datetime import datetime
import json
import os


HOST = "127.0.0.1"
PORT = 8080

LOG_FILE = "logs/deception_events.json"


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


class FakeHTTPHandler(BaseHTTPRequestHandler):

    def log_message(self, format, *args):
        pass

    def record_interaction(self, path):

        event = {

            "timestamp":
                datetime.now().isoformat(),

            "source_ip":
                self.client_address[0],

            "service":
                "FAKE_HTTP",

            "method":
                self.command,

            "path":
                path
        }

        print(
            f"[DECEPTION] HTTP | "
            f"{self.command} | "
            f"{path} | "
            f"{self.client_address[0]}"
        )

        save_event(event)

    def send_html(self, html, status=200):

        self.send_response(status)

        self.send_header(
            "Content-Type",
            "text/html; charset=utf-8"
        )

        self.end_headers()

        self.wfile.write(
            html.encode("utf-8")
        )

    def do_GET(self):

        path = urlparse(
            self.path
        ).path

        self.record_interaction(path)

        # -----------------------------------------
        # HOME
        # -----------------------------------------

        if path == "/":

            html = """
            <!DOCTYPE html>

            <html>

            <head>

                <title>
                    GHOSTMESH Device Portal
                </title>

            </head>

            <body>

                <h1>
                    GHOSTMESH Device Management
                </h1>

                <p>
                    Environment: DEMO
                </p>

                <p>
                    Network Status: ONLINE
                </p>

                <hr>

                <h2>
                    Services
                </h2>

                <ul>

                    <li>
                        <a href="/devices">
                            Device Management
                        </a>
                    </li>

                    <li>
                        <a href="/login">
                            Operator Login
                        </a>
                    </li>

                    <li>
                        <a href="/admin">
                            Administration
                        </a>
                    </li>

                </ul>

            </body>

            </html>
            """

            self.send_html(html)

        # -----------------------------------------
        # LOGIN
        # -----------------------------------------

        elif path == "/login":

            html = """
            <!DOCTYPE html>

            <html>

            <head>

                <title>
                    Operator Login
                </title>

            </head>

            <body>

                <h1>
                    Operator Login
                </h1>

                <form>

                    <label>
                        Username:
                    </label>

                    <input
                        type="text"
                        name="username"
                    >

                    <br><br>

                    <label>
                        Password:
                    </label>

                    <input
                        type="password"
                        name="password"
                    >

                    <br><br>

                    <button type="submit">
                        Login
                    </button>

                </form>

                <p>
                    Demo environment only.
                </p>

            </body>

            </html>
            """

            self.send_html(html)

        # -----------------------------------------
        # ADMIN
        # -----------------------------------------

        elif path == "/admin":

            html = """
            <!DOCTYPE html>

            <html>

            <head>

                <title>
                    Administration
                </title>

            </head>

            <body>

                <h1>
                    System Administration
                </h1>

                <h2>
                    Environment
                </h2>

                <p>
                    GHOSTMESH-DECOY
                </p>

                <p>
                    Status: ONLINE
                </p>

                <h2>
                    Available Operations
                </h2>

                <ul>

                    <li>
                        Device Status
                    </li>

                    <li>
                        Network Configuration
                    </li>

                    <li>
                        System Logs
                    </li>

                    <li>
                        Maintenance
                    </li>

                </ul>

            </body>

            </html>
            """

            self.send_html(html)

        # -----------------------------------------
        # DEVICES
        # -----------------------------------------

        elif path == "/devices":

            devices = [

                {
                    "device_id":
                        "ESP32-FAKE-01",

                    "zone":
                        "Zone-A",

                    "status":
                        "ONLINE"
                },

                {
                    "device_id":
                        "ESP32-FAKE-02",

                    "zone":
                        "Zone-B",

                    "status":
                        "ONLINE"
                },

                {
                    "device_id":
                        "SENSOR-DEMO-01",

                    "zone":
                        "Zone-C",

                    "status":
                        "ONLINE"
                }

            ]

            html = f"""
            <!DOCTYPE html>

            <html>

            <head>

                <title>
                    IoT Devices
                </title>

            </head>

            <body>

                <h1>
                    IoT Device Management
                </h1>

                <pre>
{json.dumps(devices, indent=4)}
                </pre>

            </body>

            </html>
            """

            self.send_html(html)

        # -----------------------------------------
        # 404
        # -----------------------------------------

        else:

            html = """
            <!DOCTYPE html>

            <html>

            <body>

                <h1>
                    404
                </h1>

                <p>
                    Resource not found.
                </p>

            </body>

            </html>
            """

            self.send_html(
                html,
                status=404
            )


def start_fake_http():

    server = HTTPServer(
        (HOST, PORT),
        FakeHTTPHandler
    )

    print("\n" + "=" * 55)

    print(
        "       GHOSTMESH FAKE HTTP DECOY"
    )

    print("=" * 55)

    print(
        f"[+] Server running at "
        f"http://{HOST}:{PORT}"
    )

    print("[+] Available paths:")

    print("[+] /")
    print("[+] /login")
    print("[+] /admin")
    print("[+] /devices")

    print(
        "\n[+] Press CTRL+C to stop.\n"
    )

    try:

        server.serve_forever()

    except KeyboardInterrupt:

        print(
            "\n[-] Fake HTTP server stopped."
        )

    finally:

        server.server_close()


import threading


def start_fake_http_background():

    thread = threading.Thread(
        target=start_fake_http,
        daemon=True
    )

    thread.start()

    return thread


if __name__ == "__main__":
    start_fake_http()