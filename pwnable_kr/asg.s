# ----------------------------------------------------------------------------------------
# template source - http://cs.lmu.edu/~ray/notes/gasexamples/
# gcc asm.s && ./a.out
# ----------------------------------------------------------------------------------------

        .global main
        .text
        .intel_syntax noprefix


main:
    push   ebp
    mov    ebp, esp
    sub    esp, 0x100

    mov DWORD PTR [esp + 0x10], 0x67616C66
    mov DWORD PTR [esp + 0x14], 0x2F786F62
    mov DWORD PTR [esp + 0x18], 0x41414141
    mov DWORD PTR [esp + 0x1c], 0x41414141
    mov DWORD PTR [esp + 0x20], 0x41414141
    mov DWORD PTR [esp + 0x24], 0x41414141
    mov DWORD PTR [esp + 0x28], 0x41414141
    mov DWORD PTR [esp + 0x2c], 0x41414141
    mov DWORD PTR [esp + 0x30], 0x41414141
    mov DWORD PTR [esp + 0x34], 0x41414141
    mov DWORD PTR [esp + 0x38], 0x41414141
    mov DWORD PTR [esp + 0x3c], 0x41414141
    mov DWORD PTR [esp + 0x40], 0x41414141
    mov DWORD PTR [esp + 0x44], 0x41414141
    mov DWORD PTR [esp + 0x48], 0x41414141
    mov DWORD PTR [esp + 0x4c], 0x41414141
    mov DWORD PTR [esp + 0x50], 0x41414141
    mov DWORD PTR [esp + 0x54], 0x41414141
    mov DWORD PTR [esp + 0x58], 0x00414141

    mov    edx, 0          # mode
    mov    ecx, 0          # flags  
    lea    ebx, [esp+0x10] # filename
    mov    eax, 5          # open
    int 0x80 
    
    mov    ebx, eax         # fd
    lea    ecx, [esp+0x10]  # buff
    mov    edx, 0x48       # buff_sz 
    mov    eax, 3           # read
    int 0x80
    
    mov    ebx, 1          # fd
    lea    ecx, [esp+0x10] # buff
    mov    edx, 0x48       # buff_sz 
    mov    eax, 4          # write
    int 0x80
    
    add esp, 0x100
    pop ebp
    ret
