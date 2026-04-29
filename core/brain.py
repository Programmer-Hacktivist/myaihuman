class Brain:
    def __init__(self):
        self.state = {
            "mode": "idle",
            "goal": None,
            "last_action": None
        }

    def set_goal(self, goal):
        self.state["goal"] = goal
        self.state["mode"] = "executing"

    def update(self, action):
        self.state["last_action"] = action

    def reset(self):
        self.state["mode"] = "idle"
        self.state["goal"] = None
