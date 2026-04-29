import asyncio
from voice.wake_word import listen_for_wake_word
from voice.listen import listen
from voice.speak import speak
from perception.face_auth import authenticate

async def assistant_loop(agent, personality):
    while True:
        print("Waiting wake word...")
        await asyncio.to_thread(listen_for_wake_word)

        speak("Yes?")

        if not authenticate():
            speak("Access denied")
            continue

        user_input = await asyncio.to_thread(listen)

        if not user_input:
            continue

        response = agent.handle(user_input)

        response = personality.apply(user_input, response)

        speak(response)


async def main(agent, personality, background):
    await asyncio.gather(
        assistant_loop(agent, personality),
        background.run()
    )
