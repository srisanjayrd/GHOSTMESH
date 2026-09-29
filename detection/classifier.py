class AttackClassifier:

    def classify(self, event, anomaly_score):

        ports = event.get("unique_ports", 0)
        destinations = event.get(
            "unique_destinations", 0
        )

        failed_logins = event.get(
            "failed_logins", 0
        )

        bytes_received = event.get(
            "bytes_received", 0
        )

        # Reconnaissance

        if ports >= 10 or destinations >= 8:

            return {
                "attack_type": "RECONNAISSANCE",
                "confidence": min(
                    0.60 + anomaly_score * 0.4,
                    0.99
                )
            }

        # Credential attack

        if failed_logins >= 5:

            return {
                "attack_type": "CREDENTIAL_ATTACK",
                "confidence": min(
                    0.60 + anomaly_score * 0.4,
                    0.99
                )
            }

        # Suspicious data access

        if bytes_received >= 500_000:

            return {
                "attack_type": "SUSPICIOUS_DATA_ACCESS",
                "confidence": min(
                    0.60 + anomaly_score * 0.4,
                    0.99
                )
            }

        # General anomaly

        if anomaly_score >= 0.60:

            return {
                "attack_type": "ANOMALOUS_BEHAVIOUR",
                "confidence": round(
                    anomaly_score,
                    3
                )
            }

        return {
            "attack_type": "NORMAL",
            "confidence": round(
                1 - anomaly_score,
                3
            )
        }