class SafetyGuard:
    def __init__(self):
        self.blocked = [
            "format_disk",
            "delete_system_files"
        ]

    def check(self, action):
        if action in self.blocked:
            return False, "❌ Blocked dangerous action"
        return True, ""
