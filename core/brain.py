class Brain:
    def __init__(self, state, agent, memory, tools):
        self.state = state
        self.agent = agent
        self.memory = memory
        self.tools = tools

    def decide(self, input_text):
        if self.state.get("mode") == "task":
            return self.agent.run(self.state.get("current_goal"))

        return "normal"
