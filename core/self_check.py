import json

class SelfCheck:
    def __init__(self, llm):
        self.llm = llm

    def evaluate(self, goal, action, input_data):
        prompt = f"""
You are a safety AI.

Goal: {goal}
Proposed action: {action}
Input: {input_data}

Evaluate:
1. Is this safe?
2. Is there a better alternative?
3. Should we proceed?

Return JSON:
{{
  "safe": true/false,
  "reason": "...",
  "suggestion": "optional better action"
}}
"""
        response = self.llm(prompt)

        try:
            return json.loads(response)
        except:
            return {"safe": False, "reason": "Parsing error"}
