class RiskEngine:

    def calculate(
        self,
        anomaly_score,
        failed_logins,
        unique_ports,
        unique_destinations,
        bytes_received,
        attack_type="NORMAL"
    ):

        # -----------------------------------------
        # INDIVIDUAL SECURITY SIGNALS
        # -----------------------------------------

        authentication_score = min(
            failed_logins / 20.0,
            1.0
        )

        reconnaissance_score = min(
            (
                unique_ports +
                unique_destinations
            ) / 30.0,
            1.0
        )

        data_score = min(
            bytes_received / 1_000_000.0,
            1.0
        )

        # -----------------------------------------
        # BASE RISK
        # -----------------------------------------

        risk_score = (
            0.30 * anomaly_score +
            0.25 * authentication_score +
            0.25 * reconnaissance_score +
            0.20 * data_score
        )

        # -----------------------------------------
        # ATTACK-SPECIFIC RISK
        # -----------------------------------------

        if attack_type == "RECONNAISSANCE":

            risk_score = max(
                risk_score,
                0.70
            )

        elif attack_type == "CREDENTIAL_ATTACK":

            risk_score = max(
                risk_score,
                0.75
            )

        elif attack_type == "SUSPICIOUS_DATA_ACCESS":

            risk_score = max(
                risk_score,
                0.80
            )

        elif attack_type == "LATERAL_MOVEMENT":

            risk_score = max(
                risk_score,
                0.85
            )

        # -----------------------------------------
        # MULTI-STAGE ATTACK
        # -----------------------------------------

        elif attack_type == "MULTI_STAGE_ATTACK":

            # Multiple attack phases detected.
            # Treat as critical for the demo.

            risk_score = max(
                risk_score,
                0.95
            )

        # -----------------------------------------
        # FINAL LIMIT
        # -----------------------------------------

        risk_score = min(
            max(risk_score, 0.0),
            1.0
        )

        # -----------------------------------------
        # SEVERITY
        # -----------------------------------------

        if risk_score < 0.30:

            severity = "LOW"

        elif risk_score < 0.60:

            severity = "MEDIUM"

        elif risk_score < 0.80:

            severity = "HIGH"

        else:

            severity = "CRITICAL"

        return {

            "risk_score": round(
                risk_score,
                3
            ),

            "severity": severity
        }