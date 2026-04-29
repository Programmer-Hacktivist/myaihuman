import json
import os

class TaskMemory:
    def __init__(self, path="memory/tasks.json"):
        self.path = path

        if not os.path.exists(self.path):
            with open(self.path, "w") as f:
                json.dump([], f)

    def save_task(self, goal, result, success):
        with open(self.path, "r") as f:
            data = json.load(f)

        data.append({
            "goal": goal,
            "result": result,
            "success": success
        })

        with open(self.path, "w") as f:
            json.dump(data, f, indent=2)

    def get_similar_tasks(self, goal):
        with open(self.path, "r") as f:
            data = json.load(f)

        return [t for t in data if goal.lower() in t["goal"].lower()]
