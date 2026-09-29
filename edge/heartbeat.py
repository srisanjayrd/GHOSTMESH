from datetime import datetime


def create_heartbeat(
    device_id,
    ip_address,
    temperature=25.0,
    status="ONLINE"
):

    return {

        "timestamp":
            datetime.now().isoformat(),

        "device_id":
            device_id,

        "source_ip":
            ip_address,

        "event_type":
            "HEARTBEAT",

        "status":
            status,

        "temperature":
            temperature
    }


def create_offline_event(
    device_id,
    ip_address
):

    return {

        "timestamp":
            datetime.now().isoformat(),

        "device_id":
            device_id,

        "source_ip":
            ip_address,

        "event_type":
            "DEVICE_OFFLINE",

        "status":
            "OFFLINE"
    }