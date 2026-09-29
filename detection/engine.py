from detection.features import extract_features
from detection.anomaly import AnomalyDetector
from detection.risk import RiskEngine
from detection.classifier import AttackClassifier
from detection.trust import TrustEngine


class DetectionEngine:

    def __init__(self):

        # --------------------------------
        # INITIALIZE COMPONENTS
        # --------------------------------

        self.anomaly_detector = AnomalyDetector()

        self.risk_engine = RiskEngine()

        self.classifier = AttackClassifier()

        self.trust_engine = TrustEngine()

        # --------------------------------
        # ATTACK HISTORY
        # --------------------------------
        # Stores the sequence of suspicious
        # behaviours for each source device.

        self.attack_history = {}

        # Maximum number of events remembered
        self.max_history = 10

    # --------------------------------
    # LOAD ML MODEL
    # --------------------------------

    def load_model(self):

        self.anomaly_detector.load()

    # --------------------------------
    # UPDATE ATTACK HISTORY
    # --------------------------------

    def update_attack_history(
        self,
        source_ip,
        attack_type
    ):

        # Create history for new device
        if source_ip not in self.attack_history:

            self.attack_history[source_ip] = []

        # Ignore normal events
        if attack_type == "NORMAL":
            return self.attack_history[source_ip]

        # Add new attack stage
        self.attack_history[source_ip].append(
            attack_type
        )

        # Keep only recent events
        if len(
            self.attack_history[source_ip]
        ) > self.max_history:

            self.attack_history[source_ip] = (
                self.attack_history[source_ip]
                [-self.max_history:]
            )

        return self.attack_history[source_ip]

    # --------------------------------
    # MULTI-STAGE DETECTION
    # --------------------------------

    def detect_multi_stage(
        self,
        history
    ):

        # Attack stages that we consider
        # meaningful for our demo.

        stages = [
            "RECONNAISSANCE",
            "CREDENTIAL_ATTACK",
            "LATERAL_MOVEMENT",
            "SUSPICIOUS_DATA_ACCESS"
        ]

        # Keep only recognized attack stages

        detected_stages = []

        for attack in history:

            if (
                attack in stages
                and attack not in detected_stages
            ):

                detected_stages.append(
                    attack
                )

        # If two or more different attack
        # stages occur, consider it multi-stage.

        if len(detected_stages) >= 2:

            return True, detected_stages

        return False, detected_stages

    # --------------------------------
    # MAIN ANALYSIS FUNCTION
    # --------------------------------

    def analyze(self, event):

        # ==========================================
        # STEP 1: FEATURE EXTRACTION
        # ==========================================

        features = extract_features(event)

        # ==========================================
        # STEP 2: ANOMALY DETECTION
        # ==========================================

        anomaly_result = (
            self.anomaly_detector.predict(
                features
            )
        )

        anomaly_score = anomaly_result[
            "anomaly_score"
        ]

        is_anomaly = anomaly_result[
            "is_anomaly"
        ]

        # ==========================================
        # STEP 3: ATTACK CLASSIFICATION
        # ==========================================

        classification = (
            self.classifier.classify(
                event,
                anomaly_score
            )
        )

        attack_type = classification[
            "attack_type"
        ]

        confidence = classification[
            "confidence"
        ]

        # ==========================================
        # STEP 4: UPDATE ATTACK HISTORY
        # ==========================================

        source_ip = event.get(
            "source_ip",
            "unknown"
        )

        history = self.update_attack_history(
            source_ip,
            attack_type
        )

        # ==========================================
        # STEP 5: CHECK MULTI-STAGE ATTACK
        # ==========================================

        is_multi_stage, detected_stages = (
            self.detect_multi_stage(
                history
            )
        )

        if is_multi_stage:

            attack_type = "MULTI_STAGE_ATTACK"

            # Increase confidence because
            # multiple attack stages were observed.

            confidence = min(
                0.95,
                0.70 + (
                    len(detected_stages) * 0.08
                )
            )

        # ==========================================
        # STEP 6: RISK CALCULATION
        # ==========================================

        risk_result = self.risk_engine.calculate(

            anomaly_score=anomaly_score,

            failed_logins=event.get(
                "failed_logins",
                0
            ),

            unique_ports=event.get(
                "unique_ports",
                0
            ),

            unique_destinations=event.get(
                "unique_destinations",
                0
            ),

            bytes_received=event.get(
                "bytes_received",
                0
            ),

            attack_type=attack_type
        )

        risk_score = risk_result[
            "risk_score"
        ]

        severity = risk_result[
            "severity"
        ]

        # ==========================================
        # STEP 7: TRUST SCORE
        # ==========================================

        trust_score = (
            self.trust_engine.update(
                source_ip,
                risk_score
            )
        )

        # ==========================================
        # STEP 8: SECURITY DECISION
        # ==========================================

        if risk_score >= 0.80:

            recommended_action = (
                "ACTIVATE_DECEPTION"
            )

        elif risk_score >= 0.60:

            recommended_action = "ALERT"

        elif risk_score >= 0.30:

            recommended_action = "MONITOR"

        else:

            recommended_action = "NORMAL"

        # ==========================================
        # STEP 9: FINAL RESULT
        # ==========================================

        result = {

            "timestamp": event.get(
                "timestamp"
            ),

            "source_ip": source_ip,

            "target": event.get(
                "target",
                "unknown"
            ),

            "is_anomaly": is_anomaly,

            "anomaly_score": anomaly_score,

            "risk_score": risk_score,

            "trust_score": trust_score,

            "attack_type": attack_type,

            "confidence": round(
                confidence,
                3
            ),

            "severity": severity,

            "recommended_action":
                recommended_action,

            "attack_history": history,

            "detected_stages":
                detected_stages,

            "is_multi_stage":
                is_multi_stage
        }

        return result