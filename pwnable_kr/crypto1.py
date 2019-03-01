#!/usr/bin/python

from pwn import *
context.log_level = 'error'

def send(id, pw=''):
    t = remote('pwnable.kr', 9006)
    t.sendline(id) #  id
    t.sendline(pw) #  pw
    _ = t.recvuntil('sending encrypted data (')
    edata = t.recvuntil(')\n')
    t.close()
    return edata;

cookie = ''
for i in range(49): #  cookie is 49 char long
    pre_padding = 'x' * (61 - i)
    ref_edata = send(pre_padding, '')[:128]

    for c in '_abcdefghijklmnopqrstuvwxyz-1234567890':
        edata = send(pre_padding + '--' + cookie + c)[:128]
        if edata == ref_edata:
            cookie += c
            break
    
    print 'cookie - ' + cookie
