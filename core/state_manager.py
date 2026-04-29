class StateManager:
    def __init__(self):
        self.state = {
            "mode": "idle",
            "current_goal": None,
            "last_action": None,
            "last_result": None,
            "emotion": "neutral"
        }

    def update(self, key, value):
        self.state[key] = value

    def get(self, key):
        return self.state.get(key)

    def get_all(self):
        return self.state
