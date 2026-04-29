class RiskScorer:
    def __init__(self):
        self.high_risk = ["delete", "format", "shutdown", "cmd", "powershell"]
        self.medium_risk = ["install", "modify", "kill", "taskkill"]

    def score(self, action, input_data):
        text = f"{action} {input_data}".lower()

        for k in self.high_risk:
            if k in text:
                return "high"

        for k in self.medium_risk:
            if k in text:
                return "medium"

        return "low"
