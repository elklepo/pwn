#!/usr/bin/python3
#
# CODE TAKEN FROM http://eternal.red/2018/unicorn-engine-tutorial/
# applied some modifications
#

from pwn import *
from unicorn import *
from capstone import *
from unicorn.x86_const import *

shellcode = b"\xe8\xff\xff\xff\xff\xc0\x5d\x6a\x05\x5b\x29\xdd\x83\xc5\x4e\x89\xe9\x6a\x02\x03\x0c\x24\x5b\x31\xd2\x66\xba\x12\x00\x8b\x39\xc1\xe7\x10\xc1\xef\x10\x81\xe9\xfe\xff\xff\xff\x8b\x45\x00\xc1\xe0\x10\xc1\xe8\x10\x89\xc3\x09\xfb\x21\xf8\xf7\xd0\x21\xd8\x66\x89\x45\x00\x83\xc5\x02\x4a\x85\xd2\x0f\x85\xcf\xff\xff\xff\xec\x37\x75\x5d\x7a\x05\x28\xed\x24\xed\x24\xed\x0b\x88\x7f\xeb\x50\x98\x38\xf9\x5c\x96\x2b\x96\x70\xfe\xc6\xff\xc6\xff\x9f\x32\x1f\x58\x1e\x00\xd3\x80" 


BASE = 0x400000
STACK_ADDR = 0x0
STACK_SIZE = 1024*1024

uc = Uc(UC_ARCH_X86, UC_MODE_32)
cs = Cs(CS_ARCH_X86, CS_MODE_32)

uc.mem_map(BASE, 1024*1024)
uc.mem_map(STACK_ADDR, STACK_SIZE)

uc.mem_write(BASE, shellcode)
uc.reg_write(UC_X86_REG_ESP, STACK_ADDR + STACK_SIZE // 2)

syscall_name = {1: "sys_exit", 15: "sys_chmod"}

def hook_code(uc, address, size, user_data):
    
    machine_code = uc.mem_read(address, size)
    for i in cs.disasm(machine_code, address):
        print("0x{:08x}: {} {} {}".format(
            i.address, 
            ' '.join(['{:02x}'.format(b) for b in i.bytes]).ljust(20),
            i.mnemonic,
            i.op_str))

    if machine_code == b"\xcd\x80": # int 80
        r_eax = uc.reg_read(UC_X86_REG_EAX)
        r_ebx = uc.reg_read(UC_X86_REG_EBX)
        r_ecx = uc.reg_read(UC_X86_REG_ECX)
        r_edx = uc.reg_read(UC_X86_REG_EDX)
        
        if syscall_name[r_eax] == "sys_chmod":
            s = uc.mem_read(r_ebx, 20).split(b"\x00")[0]
            print('    sys_chmod(0x{:08x}={}, {});'.format(r_ebx, s.decode(), oct(r_ecx)))
            print(oct(r_ecx))
        elif syscall_name[r_eax] == "sys_exit":
            print('    exit(0x{:08x});'.format(r_ebx))
            exit()
        uc.reg_write(UC_X86_REG_EIP, address + size)

uc.hook_add(UC_HOOK_CODE, hook_code)

uc.emu_start(BASE, BASE - 1)
