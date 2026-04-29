import asyncio

from core.memory.memory_manager import MemoryManager
from core.memory.auto_memory import extract_important_info
from brain.groq_client import ask_llm

from voice.speak import speak
from voice.listen import listen
from voice.wake_word import listen_for_wake_word

from perception.face_auth import authenticate
from core.personality import personalize_response

from core.agent import plan_task
from core.executor import execute_step

from tools.vmware import open_vmware, start_kali


# 🧠 Initialize memory
memory = MemoryManager()


# 🤖 Agent execution (async safe)
async def run_agent(goal):
    speak("Planning task...")

    steps = await asyncio.to_thread(plan_task, goal, ask_llm)

    for step in steps:
        if not step.strip():
            continue

        speak(f"Executing: {step}")
        result = await asyncio.to_thread(execute_step, step)
        print("AGENT:", result)

    speak("Task completed")


# 🧠 Main processing logic
async def process(user_input):
    text = user_input.lower()

    # 🖥️ Direct commands
    if "open kali" in text:
        await asyncio.to_thread(open_vmware)
        await asyncio.to_thread(start_kali)
        return "Starting Kali Linux"

    if "run task" in text or "do task" in text:
        await run_agent(user_input)
        return "Task execution complete"

    # 🧠 Normal AI flow
    prompt = memory.build_prompt(user_input)
    response = await asyncio.to_thread(ask_llm, prompt)

    # 💾 Store conversation
    memory.add_conversation(user_input, response)

    # 🧠 Auto-learn important info
    for key, value in extract_important_info(user_input):
        memory.remember_user(key, value)

    return response


# 🎙️ Assistant loop (non-blocking)
async def assistant_loop():
    speak("My AI Human is now online.")

    while True:
        print("Waiting for wake word...")

        # 🎧 Wake word (non-blocking)
        await asyncio.to_thread(listen_for_wake_word)

        speak("Yes, I'm listening.")

        # 👁️ Face authentication
        auth = await asyncio.to_thread(authenticate)

        if not auth:
            speak("Access denied.")
            continue

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

        # 🔊 Speak response
        await asyncio.to_thread(speak, response)


# 🚀 Entry point
if __name__ == "__main__":
    asyncio.run(assistant_loop())
