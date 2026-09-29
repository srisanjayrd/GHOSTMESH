class FakeDatabase:

    def __init__(self):

        self.data = {
            "devices": [
                {
                    "device_id": "ESP32-FAKE-01",
                    "location": "Zone-A",
                    "status": "ONLINE"
                },
                {
                    "device_id": "ESP32-FAKE-02",
                    "location": "Zone-B",
                    "status": "ONLINE"
                }
            ],

            "users": [
                {
                    "username": "operator_demo",
                    "role": "operator"
                },
                {
                    "username": "maintenance_demo",
                    "role": "maintenance"
                }
            ],

            "system": {
                "version": "GHOSTMESH-DEMO",
                "environment": "DECOY"
            }
        }

    def list_devices(self):

        return self.data["devices"]

    def list_users(self):

        return self.data["users"]

    def system_info(self):

        return self.data["system"]

    def query(self, table):

        if table in self.data:
            return self.data[table]

        return {
            "error": "TABLE_NOT_FOUND"
        }