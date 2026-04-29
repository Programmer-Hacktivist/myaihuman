def plan_task(goal, ask_llm):
    prompt = f"""
Break this goal into step-by-step actionable tasks:

Goal: {goal}

Return as numbered list.
"""
    response = ask_llm(prompt)

    steps = [line.strip() for line in response.split("\n") if line.strip()]
    return steps
