from core.memory.memory_manager import MemoryManager
from core.memory.auto_memory import extract_important_info
from brain.groq_client import ask_llm
from voice.speak import speak
from voice.listen import listen
from tools.system_control import open_app

memory = MemoryManager()

def handle_command(text):
    text = text.lower()

    if "open chrome" in text:
        open_app("chrome")
        return "Opening Chrome"

    if "open vmware" in text:
        open_app("vmware")
        return "Opening VMware"

    return None


def process(user_input):
    command = handle_command(user_input)
    if command:
        return command

    prompt = memory.build_prompt(user_input)
    response = ask_llm(prompt)

    memory.add_conversation(user_input, response)

    for key, value in extract_important_info(user_input):
        memory.remember_user(key, value)

    return response


def run():
    speak("My AI Human is online, Max.")

    while True:
        user_input = listen()

        if not user_input:
            continue

        print("You:", user_input)

        if "exit" in user_input.lower():
            speak("Goodbye Max")
            break

        response = process(user_input)
        speak(response)


if __name__ == "__main__":
    run()
