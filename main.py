import asyncio

# 🧠 Core Intelligence
from core.state_manager import StateManager
from core.brain import Brain
from core.reflection import ReflectionEngine
from core.autonomous_loop import AutonomousLoop

# 🧠 Memory Systems
from core.memory.memory_manager import MemoryManager
from core.memory.auto_memory import extract_important_info
from memory.task_memory import TaskMemory

# 🧠 AI Brain
from brain.groq_client import ask_llm

# 🎙️ Voice
from voice.speak import speak
from voice.listen import listen
from voice.wake_word import listen_for_wake_word

# 👁️ Perception
from perception.face_auth import authenticate

# 💬 Personality
from core.personality import personalize_response

# 🤖 Agent + Tools
from core.auto_agent import AutoAgent
from core.tool_setup import get_registry

# 🖥️ Tools
from tools.vmware import open_vmware, start_kali

# 🔁 Autonomous Background AI
from background.continuous_ai import ContinuousAI


# ==============================
# 🧠 INITIALIZATION
# ==============================

memory = MemoryManager()
task_memory = TaskMemory()

tools = get_registry()

state = StateManager()
agent = AutoAgent(ask_llm, memory, tools)

reflection = ReflectionEngine(ask_llm, memory, task_memory)
auto_loop = AutonomousLoop(agent, reflection, state)

brain = Brain(state, agent, memory, tools, reflection)

continuous_ai = ContinuousAI(brain, memory, state, ask_llm)


# ==============================
# 🤖 AUTONOMOUS AGENT EXECUTION
# ==============================

async def run_agent(goal):
    speak("Starting intelligent autonomous task...")

    result = await asyncio.to_thread(auto_loop.run, goal)

    speak(result)


# ==============================
# 🧠 MAIN PROCESSING LOGIC
# ==============================

async def process(user_input):
    text = user_input.lower()

    # 🖥️ Critical direct commands (fast path)
    if "open kali" in text:
        await asyncio.to_thread(open_vmware)
        await asyncio.to_thread(start_kali)
        return "Starting Kali Linux"

    # 🤖 Trigger autonomous agent
    if any(x in text for x in ["run task", "do task", "execute goal"]):
        await run_agent(user_input)
        return "Autonomous task complete"

    # 🧠 Brain-controlled decision
    response = await asyncio.to_thread(brain.handle_input, user_input)

    # 💾 Memory update
    memory.add_conversation(user_input, response)

    for key, value in extract_important_info(user_input):
        memory.remember_user(key, value)

    return response


# ==============================
# 🎙️ ASSISTANT LOOP
# ==============================

async def assistant_loop():
    speak("My AI Human is now online.")

    failed_attempts = 0

    while True:
        print("Waiting for wake word...")

        # 🎧 Wake word detection
        await asyncio.to_thread(listen_for_wake_word)

        speak("Yes, I'm listening.")

        # 👁️ Face authentication
        auth = await asyncio.to_thread(authenticate)

        if not auth:
            failed_attempts += 1
            speak("Access denied.")

            if failed_attempts >= 3:
                speak("System locked due to multiple failed attempts.")
                await asyncio.sleep(5)

            continue

        failed_attempts = 0
        speak("Access granted.")

        # 🎤 Listen
        user_input = await asyncio.to_thread(listen)

        if not user_input:
            continue

        print("You:", user_input)

        # Exit
        if "exit" in user_input.lower():
            speak("Goodbye Max.")
            break

        # 🧠 Process input
        response = await process(user_input)

        # 💬 Personality adaptation
        lower = user_input.lower()

        if any(word in lower for word in ["love", "baby", "sweet"]):
            response = personalize_response(response, "romantic")

        elif any(word in lower for word in ["command", "order", "captain"]):
            response = personalize_response(response, "command")

        else:
            response = personalize_response(response, "normal")

        # 📝 Logging
        with open("logs.txt", "a", encoding="utf-8") as f:
            f.write(f"{user_input} -> {response}\n")

        # 🔊 Speak
        await asyncio.to_thread(speak, response)


# ==============================
# 🚀 MAIN ENTRY (PARALLEL SYSTEM)
# ==============================

async def main():
    await asyncio.gather(
        assistant_loop(),
        continuous_ai.run()
    )


if __name__ == "__main__":
    asyncio.run(main())
