import json, os

class LongTermMemory:
    def __init__(self, path="memory/long_term.json"):
        self.path = path
        if not os.path.exists(path):
            json.dump([], open(path, "w"))

    def save(self, goal, steps, result):
        data = json.load(open(self.path))
        data.append({"goal": goal, "steps": steps, "result": result})
        json.dump(data, open(self.path, "w"), indent=2)

    def search(self, goal):
        data = json.load(open(self.path))
        return [x for x in data if goal.lower() in x["goal"].lower()]
