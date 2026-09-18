@echo off
setlocal

if not exist build mkdir build

nasm -f win64 tools\make_hello.asm -o build\hello.obj
if errorlevel 1 exit /b 1

link /subsystem:console /entry:main build\hello.obj kernel32.lib /out:build\hello.exe
if errorlevel 1 exit /b 1

echo [BXZ] Created build\hello.exe
