import json

class ReflectionEngine:
    def __init__(self, llm, memory):
        self.llm = llm
        self.memory = memory

    def reflect(self, goal, action, result):
        prompt = f"""
Goal: {goal}

Action taken:
{action}

Result:
{result}

Analyze:
1. Was the action successful?
2. What should be improved?
3. Next best step?

Return JSON:
{{
  "success": true/false,
  "improvement": "...",
  "next_action": "..."
}}
"""
        response = self.llm(prompt)

        try:
            data = json.loads(response)
        except:
            data = {"success": False, "next_action": "finish"}

        # Store reflection in memory
        self.memory.add_conversation(
            f"[Reflection] {goal}",
            str(data)
        )

        return data
