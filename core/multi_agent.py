class PlannerAgent:
    def __init__(self, llm):
        self.llm = llm

    def plan(self, goal):
        prompt = f"Break goal into steps: {goal}"
        return self.llm(prompt).split("\n")


class ExecutorAgent:
    def execute(self, step):
        return f"Executed: {step}"


class MemoryAgent:
    def __init__(self, memory):
        self.memory = memory

    def store(self, user_input, response):
        self.memory.add_conversation(user_input, response)


class MyAIHumanSystem:
    def __init__(self, llm, memory):
        self.planner = PlannerAgent(llm)
        self.executor = ExecutorAgent()
        self.memory = MemoryAgent(memory)

    def run_goal(self, goal):
        steps = self.planner.plan(goal)

        for step in steps:
            result = self.executor.execute(step)
            print(result)
