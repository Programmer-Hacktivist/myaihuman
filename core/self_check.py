import json

class SelfCheck:
    def __init__(self, llm):
        self.llm = llm

    def evaluate(self, goal, action, input_data):
        prompt = f"""
Goal: {goal}
Action: {action}

Safe?

Return JSON:
{{"safe": true/false}}
"""
        try:
            return json.loads(self.llm(prompt))
        except:
            return {"safe": False}
