# ----------------------------------------------------------------------------------------
# template source - http://cs.lmu.edu/~ray/notes/gasexamples/
# gcc asm.s && ./a.out
# ----------------------------------------------------------------------------------------

        .global main
        .text
        .intel_syntax noprefix
main:
    push   rbp
    mov    rbp, rsp
    sub    rsp,0x510
    mov    rax,QWORD PTR fs:0x28
    mov    QWORD PTR [rbp-0x8],rax
    xor    eax,eax
    movabs rax,0x5f73695f73696874
    movabs rdx,0x2e656c62616e7770
    mov    QWORD PTR [rbp-0x500],rax
    mov    QWORD PTR [rbp-0x4f8],rdx
    movabs rax,0x5f67616c665f726b
    movabs rdx,0x656c705f656c6966
    mov    QWORD PTR [rbp-0x4f0],rax
    mov    QWORD PTR [rbp-0x4e8],rdx
    movabs rax,0x646165725f657361
    movabs rdx,0x69665f736968745f
    mov    QWORD PTR [rbp-0x4e0],rax
    mov    QWORD PTR [rbp-0x4d8],rdx
    movabs rax,0x7972726f732e656c
    movabs rdx,0x6c69665f6568745f
    mov    QWORD PTR [rbp-0x4d0],rax
    mov    QWORD PTR [rbp-0x4c8],rdx
    movabs rax,0x695f656d616e5f65
    movabs rdx,0x6c5f797265765f73
    mov    QWORD PTR [rbp-0x4c0],rax
    mov    QWORD PTR [rbp-0x4b8],rdx
    movabs rax,0x6f6f6f6f6f6f6f6f
    movabs rdx,0x6f6f6f6f6f6f6f6f
    mov    QWORD PTR [rbp-0x4b0],rax
    mov    QWORD PTR [rbp-0x4a8],rdx
    mov    QWORD PTR [rbp-0x4a0],rax
    mov    QWORD PTR [rbp-0x498],rdx
    mov    QWORD PTR [rbp-0x490],rax
    mov    QWORD PTR [rbp-0x488],rdx
    mov    QWORD PTR [rbp-0x480],rax
    mov    QWORD PTR [rbp-0x478],rdx
    movabs rax,0x6f6f6f6f6f6f6f6f
    movabs rdx,0x303030306f6f6f6f
    mov    QWORD PTR [rbp-0x470],rax
    mov    QWORD PTR [rbp-0x468],rdx
    movabs rsi,0x3030303030303030
    movabs rdi,0x3030303030303030
    mov    QWORD PTR [rbp-0x460],rsi
    mov    QWORD PTR [rbp-0x458],rdi
    movabs rsi,0x6f6f6f3030303030
    movabs rdi,0x6f6f6f6f6f6f6f6f
    mov    QWORD PTR [rbp-0x450],rsi
    mov    QWORD PTR [rbp-0x448],rdi
    mov    QWORD PTR [rbp-0x440],rax
    mov    QWORD PTR [rbp-0x438],rdx
    movabs rax,0x3030303030303030
    movabs rdx,0x306f306f306f306f
    mov    QWORD PTR [rbp-0x430],rax
    mov    QWORD PTR [rbp-0x428],rdx
    movabs rax,0x676e6f306f306f
    mov    QWORD PTR [rbp-0x420],rax
    lea    rdx,[rbp-0x410]
    mov    eax,0x0
    mov    ecx,0x80
    mov    rdi,rdx
    rep stos QWORD PTR es:[rdi],rax
    lea    rdi,[rbp-0x500]
    mov    rsi,0x0
    mov    rax,0x2
    mov    rdx,0x0
    syscall
    mov    DWORD PTR [rbp-0x504],eax
    mov    edi,eax
    lea    rsi,[rbp-0x410]
    mov    rax,0x0
    mov    rdx,0x400
    syscall
    lea    rsi,[rbp-0x410]
    mov    rdi,0x1
    mov    rax,0x1
    mov    rdx,0x400
    syscall
    add rsp, 0x510
    pop rbp
    ret
