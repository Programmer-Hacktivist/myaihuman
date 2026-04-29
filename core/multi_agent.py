import json


class PlannerAgent:
    def __init__(self, llm):
        self.llm = llm

    def plan(self, goal):
        prompt = f"""
You are a planner AI.

Goal: {goal}

Break into steps (JSON list):
["step1", "step2"]
"""
        try:
            return json.loads(self.llm(prompt))
        except:
            return [goal]


class ExecutorAgent:
    def __init__(self, tools):
        self.tools = tools

    def execute(self, step):
        try:
            return self.tools.execute(step, "")
        except Exception as e:
            return f"Execution error: {str(e)}"


class CriticAgent:
    def __init__(self, llm):
        self.llm = llm

    def review(self, goal, step, result):
        prompt = f"""
Goal: {goal}
Step: {step}
Result: {result}

Was this good? Improve?

Return JSON:
{{
  "success": true/false,
  "feedback": "...",
  "next": "optional improved step"
}}
"""
        try:
            return json.loads(self.llm(prompt))
        except:
            return {"success": True}
