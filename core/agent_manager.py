class AgentManager:
    def __init__(self, planner, executor, memory, llm):
        self.planner = planner
        self.executor = executor
        self.memory = memory
        self.llm = llm

    def handle(self, user_input):
        if "task" in user_input.lower():
            return self.run_goal(user_input)

        return self.normal_chat(user_input)

    def run_goal(self, goal):
        steps = self.planner.plan(goal, self.llm)

        results = []
        for step in steps:
            result = self.executor.execute(step)
            results.append(result)

        return "\n".join(results)

    def normal_chat(self, user_input):
        prompt = self.memory.build_prompt(user_input)
        response = self.llm(prompt)

        self.memory.add_conversation(user_input, response)
        return response
