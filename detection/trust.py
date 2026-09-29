class TrustEngine:

    def __init__(self):

        self.trust_scores = {}

    def register_device(
        self,
        device_id,
        initial_score=100
    ):

        if device_id not in self.trust_scores:

            self.trust_scores[device_id] = initial_score

    def update(
        self,
        device_id,
        risk_score
    ):

        self.register_device(device_id)

        # Risk-based trust reduction

        reduction = risk_score * 15

        new_score = (
            self.trust_scores[device_id]
            - reduction
        )

        new_score = max(
            0,
            min(new_score, 100)
        )

        self.trust_scores[device_id] = new_score

        return round(new_score, 2)

    def get(self, device_id):

        self.register_device(device_id)

        return round(
            self.trust_scores[device_id],
            2
        )