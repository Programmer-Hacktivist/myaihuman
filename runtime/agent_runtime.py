class AgentRuntime:
    def __init__(self, planner, executor, memory):
        self.planner = planner
        self.executor = executor
        self.memory = memory

    def handle_input(self, user_input):
        if "task" in user_input:
            return self.run_goal(user_input)
        else:
            return "normal_response"

    def run_goal(self, goal):
        steps = self.planner.plan(goal)
        results = []

        for step in steps:
            result = self.executor.execute(step)
            results.append(result)

        return results
