import pefile

with open('c-shellcode.exe', 'rb') as f:
    data = f.read()
pe = pefile.PE(data=data)
oep = pe.get_offset_from_rva(pe.OPTIONAL_HEADER.AddressOfEntryPoint)
out = b'\xe9' + int(oep - pe.sections[0].PointerToRawData).to_bytes(4, 'little') \
      + data[pe.sections[0].PointerToRawData:pe.sections[0].PointerToRawData + pe.sections[0].SizeOfRawData]
out = out.rstrip(b'\x00')
if pe.FILE_HEADER.Machine == 0x8664:
    out = b'\x48\x83\xE4\xF0\x48\x83\xCC\x08' + out
print(out.hex())
with open('shellcode.txt', 'w', encoding='utf-8') as f:
    f.write(out.hex())
