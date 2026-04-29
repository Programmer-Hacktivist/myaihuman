import json


class AutoAgent:
    def __init__(self, llm, memory, tools, permission, safety, self_check, risk):
        self.llm = llm
        self.memory = memory
        self.tools = tools
        self.permission = permission
        self.safety = safety
        self.self_check = self_check
        self.risk = risk

    # =========================
    # 🧠 THINK
    # =========================
    def think(self, goal):
        tools_desc = self.tools.list_tools()

        prompt = f"""
You are an autonomous AI agent.

Goal:
{goal}

Available tools:
{tools_desc}

Return JSON:
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

    # =========================
    # 🔁 IMPROVED REFLECTION
    # =========================
    def reflect(self, goal, last_result):
        prompt = f"""
Goal: {goal}

Last result:
{last_result}

Analyze:
1. Was this successful?
2. If not, what should be done differently?
3. Suggest next action

Return JSON:
{{
  "success": true/false,
  "next_action": "...",
  "reason": "..."
}}
"""
        response = self.llm(prompt)

        try:
            return json.loads(response)
        except:
            return {"success": False}

    # =========================
    # 🤖 RUN (FULLY UPGRADED)
    # =========================
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

            # 🚫 SAFETY CHECK (hard block)
            allowed, reason = self.safety.check(action)
            if not allowed:
                print(reason)
                return reason

            # ⚖️ RISK SCORING
            risk_level = self.risk.score(action, input_data)
            print(f"⚖️ Risk Level: {risk_level}")

            # 🧠 SELF-CHECK (AI validates itself)
            check = self.self_check.evaluate(goal, action, input_data)

            if not check.get("safe", False):
                print("❌ Self-check failed:", check.get("reason"))

                suggestion = check.get("suggestion")
                if suggestion:
                    print("💡 Suggested alternative:", suggestion)

                return "Blocked by AI self-check"

            # 🔐 PERMISSION (for medium/high risk)
            if risk_level in ["medium", "high"]:
                if not self.permission.ask(action, input_data):
                    print("❌ Permission denied")
                    return "Permission denied"

            # ⚙️ EXECUTE TOOL
            try:
                result = self.tools.execute(action, input_data)
            except Exception as e:
                result = f"Execution error: {str(e)}"

            print("⚙️ Result:", result)

            # 🔁 REFLECTION (adaptive)
            reflection = self.reflect(goal, result)

            if not reflection.get("success", False):
                print("⚠️ Strategy adjustment:", reflection.get("reason"))

                alt = reflection.get("next_action")
                if alt:
                    print("🔄 Suggested next step:", alt)

            else:
                print("✅ Step successful")

        return "Max steps reached"
