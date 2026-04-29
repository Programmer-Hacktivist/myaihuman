import asyncio

class BackgroundAgent:
    def __init__(self, memory, llm):
        self.memory = memory
        self.llm = llm

    async def run(self):
        while True:
            thought = self.llm("Suggest one helpful action for user")
            print("Background AI:", thought)

            await asyncio.sleep(60)
