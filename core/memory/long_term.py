import json
import os


class LongTermMemory:
    def __init__(self, path="memory/long_term.json"):
        self.path = path

        if not os.path.exists(self.path):
            with open(self.path, "w") as f:
                json.dump([], f)

    def save(self, goal, steps, result):
        with open(self.path, "r") as f:
            data = json.load(f)

        data.append({
            "goal": goal,
            "steps": steps,
            "result": result
        })

        with open(self.path, "w") as f:
            json.dump(data, f, indent=2)

    def search(self, goal):
        with open(self.path, "r") as f:
            data = json.load(f)

        return [d for d in data if goal.lower() in d["goal"].lower()]
