import json

class ToolReasoner:
    def __init__(self, llm, tools):
        self.llm = llm
        self.tools = tools

    def decide(self, step):
        tools_desc = self.tools.list_tools()

        prompt = f"""
You are an AI tool selector.

Available tools:
{tools_desc}

User step:
{step}

Convert into JSON:
{{
  "action": "tool_name",
  "input": "what to pass"
}}
"""

        response = self.llm(prompt)

        try:
            return json.loads(response)
        except:
            return {"action": "unknown", "input": step}
