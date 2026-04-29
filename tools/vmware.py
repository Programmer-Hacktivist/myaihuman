import os

VMWARE_PATH = r"C:\Program Files (x86)\VMware\VMware Workstation\vmware.exe"
KALI_VM_PATH = r"C:\VMs\Kali Linux.vmx"

def open_vmware():
    os.startfile(VMWARE_PATH)

def start_kali():
    os.system(f'"{VMWARE_PATH}" "{KALI_VM_PATH}"')
