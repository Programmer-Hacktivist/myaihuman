from core.memory.memory_manager import MemoryManager
from core.memory.auto_memory import extract_important_info
from brain.groq_client import ask_llm
from voice.speak import speak
from voice.listen import listen

from perception.vision import detect_face_and_emotion
from core.agent import plan_task
from core.executor import execute_step
from tools.vmware import open_vmware, start_kali

memory = MemoryManager()

def run_agent(goal):
    steps = plan_task(goal, ask_llm)

    for step in steps:
        speak(f"Executing: {step}")
        result = execute_step(step)
        print(result)

def process(user_input):
    # Agent trigger
    if "do task" in user_input.lower():
        run_agent(user_input)
        return "Task execution complete"

    # Normal AI
    prompt = memory.build_prompt(user_input)
    response = ask_llm(prompt)

    memory.add_conversation(user_input, response)

    for key, value in extract_important_info(user_input):
        memory.remember_user(key, value)

    return response


def run():
    speak("My AI Human is online, Max.")

    # Face + emotion check
    user, emotion = detect_face_and_emotion()

    if user != "Max":
        speak("Unauthorized access detected.")
        return

    speak(f"Welcome {user}. Emotion detected: {emotion}")

    while True:
        user_input = listen()

        if not user_input:
            continue

        print("You:", user_input)

        if "exit" in user_input.lower():
            speak("Goodbye Max")
            break

        if "open kali" in user_input.lower():
            open_vmware()
            start_kali()
            speak("Starting Kali Linux")
            continue

        response = process(user_input)
        speak(response)


if __name__ == "__main__":
    run()
