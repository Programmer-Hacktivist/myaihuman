class PermissionManager:
    def __init__(self):
        self.sensitive_keywords = [
            "delete", "shutdown", "format",
            "install", "cmd", "powershell"
        ]

    def is_sensitive(self, action, input_data):
        text = f"{action} {input_data}".lower()
        return any(k in text for k in self.sensitive_keywords)

    def ask(self, action, input_data):
        print(f"\n⚠️ Permission required: {action} {input_data}")
        ans = input("Allow? (yes/no): ").strip().lower()
        return ans == "yes"
