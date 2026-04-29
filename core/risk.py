class RiskScorer:
    def score(self, action, input_data):
        text = f"{action} {input_data}".lower()

        if any(x in text for x in ["delete", "format"]):
            return "high"
        if any(x in text for x in ["install", "modify"]):
            return "medium"
        return "low"
