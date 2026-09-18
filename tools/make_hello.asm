; Standalone BXZ ASM smoke test.
; Produces a Windows x64 console executable when linked with kernel32.lib.

default rel

extern GetStdHandle
extern WriteFile
extern ExitProcess

global main

section .data
    message db "Hello from BXZ ASM!", 13, 10
    message_len equ $ - message

section .text

main:
    sub rsp, 40h

    mov ecx, -11
    call GetStdHandle
    mov r12, rax

    mov rcx, r12
    lea rdx, [message]
    mov r8d, message_len
    lea r9, [rsp+30h]
    mov qword [rsp+20h], 0
    call WriteFile

    xor ecx, ecx
    call ExitProcess
