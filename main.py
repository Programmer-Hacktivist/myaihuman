import asyncio
import sys

# 🧠 Systems
from core.memory.memory_manager import MemoryManager
from core.memory.auto_memory import extract_important_info

from brain.groq_client import ask_llm

# 🎙️ Voice
from voice.speak import speak
from voice.listen import listen
from voice.wake_word import listen_for_wake_word

# 👁️ Auth
from perception.face_auth import authenticate

# 💬 Personality
from core.personality import personalize_response

# 🤖 Agent System
from core.agent_system import AgentSystem
from core.tool_setup import get_registry

# 🖥️ HUD
from ui.hud import start_hud


# =========================
# 🧠 INIT
# =========================

memory = MemoryManager()
tools = get_registry()

agent_system = AgentSystem(ask_llm, tools)


# =========================
# 🖥️ START HUD
# =========================

app, hud = start_hud()


# =========================
# 🤖 AGENT WITH HUD HOOK
# =========================

def run_agent_with_hud(goal):
    hud.update_state(thought="Planning...", action="-", result="-")

    result = agent_system.run(goal)

    hud.update_state(
        thought="Completed",
        action="finish",
        result=result
    )

    return result


# =========================
# 🧠 PROCESS
# =========================

async def process(user_input):
    text = user_input.lower()

    if any(x in text for x in ["run task", "do task", "execute goal"]):
        result = await asyncio.to_thread(run_agent_with_hud, user_input)
        return result

    # Normal AI
    prompt = memory.build_prompt(user_input)
    response = await asyncio.to_thread(ask_llm, prompt)

    memory.add_conversation(user_input, response)

    for k, v in extract_important_info(user_input):
        memory.remember_user(k, v)

    return response


# =========================
# 🎙️ LOOP
# =========================

async def assistant_loop():
    speak("My AI Human is online.")

    while True:
        await asyncio.to_thread(listen_for_wake_word)

        speak("Yes, I'm listening.")

        if not await asyncio.to_thread(authenticate):
            speak("Access denied.")
            continue

        speak("Access granted.")

        user_input = await asyncio.to_thread(listen)

        if not user_input:
            continue

        if "exit" in user_input.lower():
            speak("Goodbye Max.")
            break

        response = await process(user_input)

        response = personalize_response(response, "normal")

        await asyncio.to_thread(speak, response)


# =========================
# 🚀 RUN BOTH HUD + AI
# =========================

async def main():
    asyncio.create_task(assistant_loop())

    # Run Qt loop safely
    while True:
        app.processEvents()
        await asyncio.sleep(0.01)


if __name__ == "__main__":
    asyncio.run(main())
