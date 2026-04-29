import json

class AutoAgent:
    def __init__(self, llm, memory, tools):
        self.llm = llm
        self.memory = memory
        self.tools = tools

    def think(self, goal):
        tools_desc = self.tools.list_tools()

        prompt = f"""
You are an autonomous AI agent.

Goal:
{goal}

Available tools:
{tools_desc}

Decide next action in JSON:

{{
  "thought": "...",
  "action": "tool_name or 'finish'",
  "input": "input for tool"
}}
"""
        response = self.llm(prompt)

        try:
            return json.loads(response)
        except:
            return {
                "thought": "Parsing error",
                "action": "finish",
                "input": ""
            }

    def reflect(self, goal, last_result):
        prompt = f"""
Goal: {goal}

Last result:
{last_result}

Should we continue or finish?
Answer in JSON:
{{
  "continue": true/false,
  "reason": "..."
}}
"""
        response = self.llm(prompt)

        try:
            return json.loads(response)
        except:
            return {"continue": False}

    def run(self, goal, max_steps=5):
        print(f"\n🎯 Goal: {goal}")

        for step in range(max_steps):
            decision = self.think(goal)

            print("🧠 Thought:", decision["thought"])

            if decision["action"] == "finish":
                print("✅ Finished")
                return "Task completed"

            # Execute tool
            result = self.tools.execute(
                decision["action"],
                decision["input"]
            )

            print("⚙️ Result:", result)

            # Reflect
            reflection = self.reflect(goal, result)

            if not reflection.get("continue", False):
                print("🛑 Stopping:", reflection.get("reason"))
                return result

        return "Max steps reached"
