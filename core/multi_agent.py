import json

class PlannerAgent:
    def __init__(self, llm):
        self.llm = llm

    def plan(self, goal):
        prompt = f"Break goal into steps: {goal}"
        try:
            return json.loads(self.llm(prompt))
        except:
            return [goal]


class ExecutorAgent:
    def __init__(self, tools):
        self.tools = tools

    def execute(self, action, input_data):
        return self.tools.execute(action, input_data)


class CriticAgent:
    def __init__(self, llm):
        self.llm = llm

    def review(self, goal, step, result):
        prompt = f"""
Goal: {goal}
Step: {step}
Result: {result}

Return JSON:
{{"success": true/false, "feedback": "..."}}
"""
        try:
            return json.loads(self.llm(prompt))
        except:
            return {"success": True}
