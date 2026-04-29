import asyncio

# 🧠 Core Systems
from core.state_manager import StateManager
from core.memory.memory_manager import MemoryManager
from core.memory.auto_memory import extract_important_info

# 🤖 AI Brain
from brain.groq_client import ask_llm

# 🎙️ Voice
from voice.speak import speak
from voice.listen import listen
from voice.wake_word import listen_for_wake_word

# 👁️ Face Auth
from perception.face_auth import authenticate

# 💬 Personality
from core.personality import personalize_response

# 🛠️ Tools + Agent
from core.auto_agent import AutoAgent
from core.tool_setup import get_registry

# 🔐 Safety System
from core.permission import PermissionManager
from core.safety import SafetyGuard

# 🖥️ Tools
from tools.vmware import open_vmware, start_kali


# =========================
# 🧠 INITIALIZATION
# =========================

memory = MemoryManager()
tools = get_registry()

permission = PermissionManager()
safety = SafetyGuard()

agent = AutoAgent(
    ask_llm,
    memory,
    tools,
    permission,
    safety
)


# =========================
# 🤖 RUN AGENT
# =========================

async def run_agent(goal):
    speak("Starting autonomous task...")

    result = await asyncio.to_thread(agent.run, goal)

    speak(result)


# =========================
# 🧠 PROCESS INPUT
# =========================

async def process(user_input):
    text = user_input.lower()

    # 🖥️ Direct command
    if "open kali" in text:
        await asyncio.to_thread(open_vmware)
        await asyncio.to_thread(start_kali)
        return "Starting Kali Linux"

    # 🤖 Agent trigger
    if any(x in text for x in ["run task", "do task", "execute goal"]):
        await run_agent(user_input)
        return "Task execution complete"

    # 🧠 Normal chat
    prompt = memory.build_prompt(user_input)
    response = await asyncio.to_thread(ask_llm, prompt)

    memory.add_conversation(user_input, response)

    for key, value in extract_important_info(user_input):
        memory.remember_user(key, value)

    return response


# =========================
# 🎙️ MAIN LOOP
# =========================

async def assistant_loop():
    speak("My AI Human is now online.")

    failed_attempts = 0

    while True:
        print("Waiting for wake word...")

        await asyncio.to_thread(listen_for_wake_word)

        speak("Yes, I'm listening.")

        # 👁️ Face Auth
        auth = await asyncio.to_thread(authenticate)

        if not auth:
            failed_attempts += 1
            speak("Access denied.")

            if failed_attempts >= 3:
                speak("System locked.")
                await asyncio.sleep(5)

            continue

        failed_attempts = 0
        speak("Access granted.")

        # 🎤 Listen
        user_input = await asyncio.to_thread(listen)

        if not user_input:
            continue

        print("You:", user_input)

        if "exit" in user_input.lower():
            speak("Goodbye Max.")
            break

        # 🧠 Process
        response = await process(user_input)

        # 💬 Personality
        lower = user_input.lower()

        if any(w in lower for w in ["love", "baby", "sweet"]):
            response = personalize_response(response, "romantic")
        elif any(w in lower for w in ["command", "captain", "order"]):
            response = personalize_response(response, "command")
        else:
            response = personalize_response(response, "normal")

        # 📝 Log
        with open("logs.txt", "a", encoding="utf-8") as f:
            f.write(f"{user_input} -> {response}\n")

        # 🔊 Speak
        await asyncio.to_thread(speak, response)


# =========================
# 🚀 ENTRY
# =========================

if __name__ == "__main__":
    asyncio.run(assistant_loop())
