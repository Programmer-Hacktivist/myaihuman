import json


class AutoAgent:
    def __init__(self, llm, memory, tools, permission, safety):
        self.llm = llm
        self.memory = memory
        self.tools = tools
        self.permission = permission
        self.safety = safety

    # 🧠 THINK
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

    # 🔁 REFLECT
    def reflect(self, goal, last_result):
        prompt = f"""
Goal: {goal}

Last result:
{last_result}

Should we continue or finish?

Return JSON:
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

    # 🤖 RUN AGENT
    def run(self, goal, max_steps=5):
        print(f"\n🎯 Goal: {goal}")

        for step in range(max_steps):
            decision = self.think(goal)

            thought = decision.get("thought", "")
            action = decision.get("action", "finish")
            input_data = decision.get("input", "")

            print("🧠 Thought:", thought)

            if action == "finish":
                print("✅ Finished")
                return "Task completed"

            # 🚫 SAFETY CHECK
            allowed, reason = self.safety.check(action)
            if not allowed:
                print(reason)
                return reason

            # 🔐 PERMISSION CHECK
            if self.permission.is_sensitive(action, input_data):
                if not self.permission.ask(action, input_data):
                    print("❌ Permission denied by user")
                    return "Permission denied"

            # ⚙️ EXECUTE TOOL (SAFE EXECUTION)
            try:
                result = self.tools.execute(action, input_data)
            except Exception as e:
                result = f"Execution error: {str(e)}"

            print("⚙️ Result:", result)

            # 🔁 REFLECTION
            reflection = self.reflect(goal, result)

            if not reflection.get("continue", False):
                print("🛑 Stopping:", reflection.get("reason"))
                return result

        return "Max steps reached"
