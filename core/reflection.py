class ReflectionEngine:
    def __init__(self, llm, memory, task_memory):
        self.llm = llm
        self.memory = memory
        self.task_memory = task_memory

    def reflect(self, goal, action, result):
        prompt = f"""
Goal: {goal}

Action: {action}
Result: {result}

Was it successful? What next?

Return JSON:
{{
  "success": true/false,
  "next_action": "..."
}}
"""
        response = self.llm(prompt)

        import json
        try:
            data = json.loads(response)
        except:
            data = {"success": False}

        # 📚 Save learning
        self.task_memory.save_task(
            goal,
            result,
            data.get("success", False)
        )

        return data
