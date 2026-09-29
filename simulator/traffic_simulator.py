from datetime import datetime


def normal():

    return {
        "timestamp": datetime.now().isoformat(),
        "source_ip": "192.168.50.10",
        "target": "ESP32-01",

        "connection_count": 6,
        "unique_ports": 1,
        "unique_destinations": 1,

        "failed_logins": 0,

        "bytes_sent": 13000,
        "bytes_received": 10000,

        "connection_rate": 0.6
    }


def reconnaissance():

    return {
        "timestamp": datetime.now().isoformat(),
        "source_ip": "192.168.50.10",
        "target": "NETWORK",

        "connection_count": 80,
        "unique_ports": 25,
        "unique_destinations": 12,

        "failed_logins": 0,

        "bytes_sent": 50000,
        "bytes_received": 20000,

        "connection_rate": 8.0
    }


def credential_attack():

    return {
        "timestamp": datetime.now().isoformat(),
        "source_ip": "192.168.50.10",
        "target": "ESP32-01",

        "connection_count": 50,
        "unique_ports": 2,
        "unique_destinations": 1,

        "failed_logins": 30,

        "bytes_sent": 30000,
        "bytes_received": 15000,

        "connection_rate": 5.0
    }


def data_access():

    return {
        "timestamp": datetime.now().isoformat(),
        "source_ip": "192.168.50.10",
        "target": "FAKE-DATABASE",

        "connection_count": 30,
        "unique_ports": 3,
        "unique_destinations": 2,

        "failed_logins": 0,

        "bytes_sent": 100000,
        "bytes_received": 900000,

        "connection_rate": 3.0
    }