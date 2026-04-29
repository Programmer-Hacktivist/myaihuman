class Personality:

    def apply(self, user_input, response):
        text = user_input.lower()

        if any(x in text for x in ["baby", "baal"]):
            return f"baby, {response}"

        if any(x in text for x in ["captain", "command"]):
            return f"captain, {response}"

        return response
