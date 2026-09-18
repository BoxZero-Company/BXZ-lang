# BXZ x86-64 Backend

Target pipeline:

BXZ source -> Lexer -> Parser -> AST -> BXZ IR -> x86-64 machine code -> PE32+ writer -> Windows EXE

The final compiler target is to let end users build BXZ programs without Rust, NASM, CMake, or Visual Studio Build Tools installed.
