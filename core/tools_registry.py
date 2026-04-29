class ToolRegistry:
    def __init__(self):
        self.tools = {}

    def register(self, name, func, description):
        self.tools[name] = {
            "func": func,
            "description": description
        }

    def list_tools(self):
        return {
            name: tool["description"]
            for name, tool in self.tools.items()
        }

    def execute(self, name, *args):
        if name not in self.tools:
            return f"Tool {name} not found"

        return self.tools[name]["func"](*args)
