import time
from core.agent_system import AgentSystem
from brain.groq_client import ask_llm
from core.tool_setup import get_registry

tools = get_registry()
agent = AgentSystem(ask_llm, tools)

def run_service():
    print("Background AI Service Started")

    while True:
        # autonomous thinking placeholder
        print("AI idle...")
        time.sleep(10)

if __name__ == "__main__":
    run_service()
