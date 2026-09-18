; BXZ x86-64 Windows bootstrap runtime
; NASM syntax
; This file is a real Windows x64 console entry point.
;
; Build with:
;   nasm -f win64 asm\x86_64\bxz.asm -o build\bxz.obj
;   link /subsystem:console /entry:bxz_entry build\bxz.obj kernel32.lib /out:build\bxz.exe

default rel

extern GetStdHandle
extern WriteFile
extern ExitProcess

global bxz_entry

section .data
    bxz_banner db "BXZ runtime v1.2.2.1", 13, 10
    bxz_banner_len equ $ - bxz_banner

section .text

bxz_entry:
    sub rsp, 40h

    ; HANDLE stdout = GetStdHandle(STD_OUTPUT_HANDLE)
    mov ecx, -11
    call GetStdHandle

    ; Save stdout handle
    mov r12, rax

    ; WriteFile(stdout, banner, length, &written, NULL)
    mov rcx, r12
    lea rdx, [bxz_banner]
    mov r8d, bxz_banner_len
    lea r9, [rsp+30h]
    mov qword [rsp+20h], 0
    call WriteFile

    xor ecx, ecx
    call ExitProcess

    int3
