class PermissionManager:
    def is_sensitive(self, action, input_data):
        risky = ["delete", "shutdown", "format"]
        text = f"{action} {input_data}".lower()
        return any(x in text for x in risky)

    def ask(self, action, input_data):
        print(f"⚠️ अनुमति चाहिए: {action}")
        return input("Allow? (yes/no): ").lower() == "yes"
