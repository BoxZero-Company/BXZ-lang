@echo off
setlocal

if not exist build mkdir build

where nasm >nul 2>nul
if errorlevel 1 (
  echo [BXZ] NASM not found in PATH.
  exit /b 1
)

nasm -f win64 asm\x86_64\bxz_runtime.asm -o build\bxz_runtime.obj
if errorlevel 1 exit /b 1

echo [BXZ] Assembly runtime object created.
