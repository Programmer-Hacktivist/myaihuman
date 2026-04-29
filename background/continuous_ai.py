import asyncio

class ContinuousAI:
    def __init__(self, brain, memory, state, llm):
        self.brain = brain
        self.memory = memory
        self.state = state
        self.llm = llm

    async def run(self):
        while True:
            if self.state.get("mode") == "idle":
                thought = await asyncio.to_thread(
                    self.llm,
                    "Suggest one useful action for the user"
                )

                print("🤖 Autonomous Thought:", thought)

                if "do" in thought.lower():
                    print("⚡ Executing autonomous action...")
                    await asyncio.to_thread(
                        self.brain.start_goal,
                        thought
                    )

            await asyncio.sleep(30)
