import re

with open('c-shellcode.asm', 'r', encoding='utf-8') as f:
    data = f.read()
data = data.replace('INCLUDELIB LIBCMT', '').replace('INCLUDELIB OLDNAMES', '')
data = re.sub(r'(;\tCOMDAT pdata.*xdata\tENDS)', '', data, flags=re.DOTALL)
data = re.sub(r'\bgs:(\d+)', r'gs:[\1]', data)
data = re.sub(r'\bfs:(\d+)', r'fs:[\1]', data)
data = re.sub(r'(.*\n)(.*\bfs:\[\d+]\n)(.*\n)', r'\1ASSUME FS:NOTHING\n\2ASSUME FS:ERROR\n\3', data, flags=re.MULTILINE)
data = re.sub(r'OFFSET FLAT:', r'OFFSET ', data)
with open('c-shellcode.asm', 'w', encoding='utf-8') as f:
    f.write(data)
