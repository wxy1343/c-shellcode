@echo off
del /f /q c-shellcode.exe c-shellcode.asm shellcode.txt 2>NUL

for /f "tokens=*" %%i IN (
    '"%ProgramFiles(x86)%\Microsoft Visual Studio\Installer\vswhere.exe" -latest -prerelease -products * ^
    -requires Microsoft.VisualStudio.Component.VC.Tools.x86.x64 ^
    -version [16^,18^) ^
    -property installationPath'
) do set vsBase=%%i
call "%vsBase%\vc\Auxiliary\Build\vcvarsall.bat" x64 %*

chcp 65001
cl.exe /c /FA /GS- c-shellcode.cpp
python 1.py
ml64.exe c-shellcode.asm /link /entry:main
python 2.py
pause