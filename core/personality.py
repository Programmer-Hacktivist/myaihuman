import random

def get_ai_name(context="normal"):
    if context == "romantic":
        return "baby"
    elif context == "command":
        return "captain"
    return random.choice(["sir", "boss"])


def personalize_response(text, context="normal"):
    name = get_ai_name(context)
    return f"{name}, {text}"
