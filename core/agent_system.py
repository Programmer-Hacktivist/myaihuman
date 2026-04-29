from core.multi_agent import PlannerAgent, ExecutorAgent, CriticAgent
from memory.long_term import LongTermMemory
from ui.hud import HUD


class AgentSystem:
    def __init__(self, llm, tools):
        self.planner = PlannerAgent(llm)
        self.executor = ExecutorAgent(tools)
        self.critic = CriticAgent(llm)
        self.memory = LongTermMemory()
        self.hud = HUD()

    def run(self, goal):
        self.hud.show("🎯 Goal", goal)

        # 📚 Check past memory
        past = self.memory.search(goal)
        if past:
            self.hud.show("📚 Memory Found", past[0]["steps"])

        # 🧠 PLAN
        steps = self.planner.plan(goal)
        self.hud.show("🧠 Plan", steps)

        results = []

        for step in steps:
            self.hud.show("⚙️ Executing", step)

            result = self.executor.execute(step)
            results.append(result)

            self.hud.show("📥 Result", result)

            # 🔁 CRITIC
            review = self.critic.review(goal, step, result)

            if not review.get("success", True):
                self.hud.show("⚠️ Critic", review.get("feedback"))

                improved = review.get("next")
                if improved:
                    self.hud.show("🔄 Retry", improved)
                    result = self.executor.execute(improved)

        final = " | ".join(results)

        # 📚 Save learning
        self.memory.save(goal, steps, final)

        self.hud.show("✅ Done", final)

        return final
