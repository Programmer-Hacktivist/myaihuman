from core.tools_registry import ToolRegistry
from tools.system_control import open_app
from tools.vmware import open_vmware, start_kali

registry = ToolRegistry()

registry.register(
    "open_app",
    open_app,
    "Open an application by name"
)

registry.register(
    "open_vmware",
    open_vmware,
    "Open VMware"
)

registry.register(
    "start_kali",
    start_kali,
    "Start Kali Linux VM"
)

def get_registry():
    return registry
