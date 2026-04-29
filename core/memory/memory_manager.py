from .short_term import ShortTermMemory
from .long_term import LongTermMemory
from .semantic import SemanticMemory

class MemoryManager:
    def __init__(self):
        self.short = ShortTermMemory()
        self.long = LongTermMemory()
        self.semantic = SemanticMemory()

    def add_conversation(self, user_input, ai_response):
        self.short.add("user", user_input)
        self.short.add("assistant", ai_response)

        if len(user_input.split()) > 3:
            self.semantic.add(user_input)

    def remember_user(self, key, value):
        self.long.set(key, value)

    def build_prompt(self, user_input):
        return f"""
User Profile:
{self.long.get_all()}

Recent:
{self.short.get_context()}

Relevant:
{self.semantic.search(user_input)}

User: {user_input}
"""
