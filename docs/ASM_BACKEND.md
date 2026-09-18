# BXZ ASM backend

Target: Windows x64 / Microsoft x64 ABI.

The Assembly runtime currently calls:
- GetStdHandle
- WriteFile
- ExitProcess

Next: Rust x86-64 machine-code emission and an internal PE32+ writer so
`bxz build program.bxz` can produce an executable without an external linker.
