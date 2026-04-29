from ui.hud import start_hud
from core.agent_system import AgentSystem
from brain.groq_client import ask_llm
from core.tool_setup import get_registry

tools = get_registry()

def main():
    app, hud = start_hud()

    agent = AgentSystem(ask_llm, tools, hud=hud)

    # simple demo loop
    def run():
        while True:
            user = input(">> ")
            if user == "exit":
                break
            result = agent.run(user)
            print(result)

    import threading
    threading.Thread(target=run, daemon=True).start()

    app.exec()

if __name__ == "__main__":
    main()
