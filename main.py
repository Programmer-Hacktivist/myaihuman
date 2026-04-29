import asyncio

from core.memory.memory_manager import MemoryManager
from core.memory.auto_memory import extract_important_info
from brain.groq_client import ask_llm

from voice.speak import speak
from voice.listen import listen
from voice.wake_word import listen_for_wake_word

from perception.face_auth import authenticate
from core.personality import personalize_response

from core.auto_agent import AutoAgent
from core.tool_setup import get_registry

from tools.vmware import open_vmware, start_kali


# 🧠 Initialize memory
memory = MemoryManager()

# 🛠️ Tool system
tools = get_registry()

# 🤖 Autonomous agent
agent = AutoAgent(ask_llm, memory, tools)


# 🤖 Run autonomous agent
async def run_agent(goal):
    speak("Starting autonomous task...")

    result = await asyncio.to_thread(agent.run, goal)

    speak(result)


# 🧠 Main processing logic
async def process(user_input):
    text = user_input.lower()

    # 🖥️ Direct critical commands (fast path)
    if "open kali" in text:
        await asyncio.to_thread(open_vmware)
        await asyncio.to_thread(start_kali)
        return "Starting Kali Linux"

    # 🤖 Autonomous agent trigger
    if any(x in text for x in ["run task", "do task", "execute goal"]):
        await run_agent(user_input)
        return "Task execution complete"

    # 🧠 Normal AI conversation
    prompt = memory.build_prompt(user_input)
    response = await asyncio.to_thread(ask_llm, prompt)

    # 💾 Store memory
    memory.add_conversation(user_input, response)

    for key, value in extract_important_info(user_input):
        memory.remember_user(key, value)

    return response


# 🎙️ Assistant loop
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
                speak("Multiple failed attempts detected. System locked.")
                await asyncio.sleep(5)

            continue

        failed_attempts = 0
        speak("Access granted.")

        # 🎤 Listen for command
        user_input = await asyncio.to_thread(listen)

        if not user_input:
            continue

        print("You:", user_input)

        # Exit condition
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

        # 📝 Logging (important)
        with open("logs.txt", "a", encoding="utf-8") as f:
            f.write(f"{user_input} -> {response}\n")

        # 🔊 Speak response
        await asyncio.to_thread(speak, response)


# 🚀 Entry point
if __name__ == "__main__":
    asyncio.run(assistant_loop())
