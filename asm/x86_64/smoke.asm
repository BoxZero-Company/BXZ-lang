; Standalone BXZ x86-64 Windows smoke executable
default rel
extern GetStdHandle
extern WriteFile
extern ExitProcess
global bxz_entry

section .data
msg db "BXZ ASM OK", 13, 10
msg_len equ $-msg

section .text
bxz_entry:
    sub rsp, 40h
    mov ecx, -11
    call GetStdHandle
    mov r12, rax
    mov rcx, r12
    lea rdx, [msg]
    mov r8d, msg_len
    lea r9, [rsp+30h]
    mov qword [rsp+20h], 0
    call WriteFile
    xor ecx, ecx
    call ExitProcess
