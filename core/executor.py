from tools.system_control import open_app

def execute_step(step):
    step = step.lower()

    if "open vmware" in step:
        open_app("vmware")
        return "VMware opened"

    if "open chrome" in step:
        open_app("chrome")
        return "Chrome opened"

    return f"Executed: {step}"
