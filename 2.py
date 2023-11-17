import pefile

with open('c-shellcode.exe', 'rb') as f:
    data = f.read()
pe = pefile.PE(data=data)
oep = pe.get_offset_from_rva(pe.OPTIONAL_HEADER.AddressOfEntryPoint)
out = (b'\xe9' + int(oep - pe.sections[0].PointerToRawData).to_bytes(4, 'little')).hex() \
      + data[pe.sections[0].PointerToRawData:pe.sections[0].PointerToRawData + pe.sections[0].SizeOfRawData].hex()
out = out.rstrip('00')
print(out)
with open('shellcode.txt', 'w', encoding='utf-8') as f:
    f.write(out)
