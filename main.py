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


# Initialize memory
memory = MemoryManager()


# 🤖 Agent execution
def run_agent(goal):
    speak("Planning task...")

    steps = plan_task(goal, ask_llm)

    for step in steps:
        if not step.strip():
            continue

        speak(f"Executing: {step}")
        result = execute_step(step)
        print("AGENT:", result)

    speak("Task completed")


# 🧠 Main processing logic
def process(user_input):
    text = user_input.lower()

    # 🖥️ Direct commands
    if "open kali" in text:
        open_vmware()
        start_kali()
        return "Starting Kali Linux"

    if "run task" in text or "do task" in text:
        run_agent(user_input)
        return "Task execution complete"

    # 🧠 Normal AI flow
    prompt = memory.build_prompt(user_input)
    response = ask_llm(prompt)

    # 💾 Store conversation
    memory.add_conversation(user_input, response)

    # 🧠 Auto-learn important info
    for key, value in extract_important_info(user_input):
        memory.remember_user(key, value)

    return response


# 🎙️ Main assistant loop
def run():
    speak("My AI Human is now online.")

    while True:
        # 🎧 Wait for wake word
        print("Waiting for wake word...")
        listen_for_wake_word()

        speak("Yes, I'm listening.")

        # 👁️ Face authentication
        if not authenticate():
            speak("Access denied.")
            continue

        speak("Access granted.")

        # 🎤 Listen for command
        user_input = listen()

        if not user_input:
            continue

        print("You:", user_input)

        # Exit condition
        if "exit" in user_input.lower():
            speak("Goodbye Max.")
            break

        # 🧠 Process input
        response = process(user_input)

        # 💬 Personality adaptation
        if any(word in user_input.lower() for word in ["love", "baby", "sweet"]):
            response = personalize_response(response, "romantic")

        elif any(word in user_input.lower() for word in ["command", "order", "captain"]):
            response = personalize_response(response, "command")

        else:
            response = personalize_response(response, "normal")

        # 🔊 Speak response
        speak(response)


# 🚀 Entry point
if __name__ == "__main__":
    run()
