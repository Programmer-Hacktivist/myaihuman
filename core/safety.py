class SafetyGuard:
    def check(self, action):
        blocked = ["format_disk"]
        if action in blocked:
            return False, "Blocked dangerous action"
        return True, ""
