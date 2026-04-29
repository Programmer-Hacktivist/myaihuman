from core.multi_agent import PlannerAgent, ExecutorAgent, CriticAgent
from core.tool_reasoner import ToolReasoner
from core.brain import Brain
from memory.long_term import LongTermMemory

class AgentSystem:
    def __init__(self, llm, tools, hud=None):
        self.planner = PlannerAgent(llm)
        self.executor = ExecutorAgent(tools)
        self.critic = CriticAgent(llm)

        self.reasoner = ToolReasoner(llm, tools)
        self.memory = LongTermMemory()
        self.brain = Brain()

        self.hud = hud

    def hud_update(self, t=None,a=None,r=None):
        if self.hud:
            self.hud.update_state(t,a,r)

    def run(self, goal):
        self.brain.set_goal(goal)

        steps = self.planner.plan(goal)
        results = []

        for step in steps:
            self.hud_update(f"Step: {step}")

            decision = self.reasoner.decide(step)
            action = decision["action"]
            inp = decision["input"]

            self.brain.update(action)
            self.hud_update(step, action)

            result = self.executor.execute(action, inp)
            results.append(result)

            self.hud_update(step, action, result)

            review = self.critic.review(goal, step, result)

        final = " | ".join(results)
        self.memory.save(goal, steps, final)

        self.hud_update("Done","finish",final)
        self.brain.reset()

        return final
