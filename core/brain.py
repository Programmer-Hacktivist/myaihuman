class Brain:
    def __init__(self, state, agent, memory, tools, reflection):
        self.state = state
        self.agent = agent
        self.memory = memory
        self.tools = tools
        self.reflection = reflection

    def handle_input(self, user_input):
        # Save last input
        self.state.update("last_input", user_input)

        # If already in task mode → continue goal
        if self.state.get("mode") == "task":
            return self.run_current_goal()

        # Otherwise start new goal
        return self.start_goal(user_input)

    def start_goal(self, goal):
        self.state.update("mode", "task")
        self.state.update("current_goal", goal)

        return self.run_current_goal()

    def run_current_goal(self):
        goal = self.state.get("current_goal")

        result = self.agent.run(goal)

        self.state.update("last_result", result)
        self.state.update("mode", "idle")

        return result
