class AutonomousLoop:
    def __init__(self, agent, reflection, state):
        self.agent = agent
        self.reflection = reflection
        self.state = state

    def run(self, goal, max_cycles=5):
        print(f"\n🎯 Starting Goal: {goal}")

        self.state.update("mode", "task")
        self.state.update("current_goal", goal)

        for cycle in range(max_cycles):
            print(f"\n🔁 Cycle {cycle+1}")

            # 🧠 THINK + ACT
            decision = self.agent.think(goal)

            action = decision.get("action")
            input_data = decision.get("input")

            if action == "finish":
                print("✅ Goal finished")
                break

            result = self.agent.tools.execute(action, input_data)

            print("⚙️ Action:", action)
            print("📥 Result:", result)

            # 🧠 Update state
            self.state.update("last_action", action)
            self.state.update("last_result", result)

            # 🔁 REFLECT
            reflection = self.reflection.reflect(goal, action, result)

            print("🧠 Reflection:", reflection)

            if not reflection.get("success", False):
                print("⚠️ Adjusting strategy...")

            if reflection.get("next_action") == "finish":
                print("🛑 Ending task based on reflection")
                break

        self.state.update("mode", "idle")
        return "Autonomous task complete"
