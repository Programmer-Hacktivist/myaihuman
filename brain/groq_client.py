from groq import Groq
from config.settings import GROQ_API_KEY

client = Groq(api_key=GROQ_API_KEY)

def ask_llm(prompt):
    response = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=[
            {"role": "system", "content": "You are My AI Human, a smart personal AI assistant."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content
