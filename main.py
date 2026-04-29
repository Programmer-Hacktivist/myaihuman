import asyncio
from brain.groq_client import ask_llm
from core.tool_setup import get_registry
from core.agent_system import AgentSystem
from ui.hud import start_hud

tools = get_registry()

app, hud = start_hud()

agent = AgentSystem(ask_llm, tools, hud=hud)

async def main_loop():
    while True:
        user = input(">> ")

        if user == "exit":
            break

        result = await asyncio.to_thread(agent.run, user)
        print("AI:", result)

async def main():
    asyncio.create_task(main_loop())

    while True:
        app.processEvents()
        await asyncio.sleep(0.01)

if __name__ == "__main__":
    asyncio.run(main())
