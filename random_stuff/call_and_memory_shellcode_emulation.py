#!/usr/bin/python3
#
# capstone + unicorn useful refs:
# https://www.capstone-engine.org/lang_python.html
# https://github.com/unicorn-engine/unicorn/blob/master/bindings/python/sample_x86.py
# https://github.com/unicorn-engine/unicorn/blob/master/samples/sample_x86.c
# https://github.com/unicorn-engine/unicorn/blob/master/bindings/python/unicorn/unicorn_const.py
#

from pwn import *
from unicorn import *
from capstone import *
from capstone.x86 import *
from unicorn.x86_const import *

with open('shellcode', 'rb') as f:
    shellcode = f.read()

IMG_BASE = 0x400000
IMG_SIZE = 1024*1024
STACK_BASE = 0xf00000
STACK_SIZE = 1024*1024

uc = Uc(UC_ARCH_X86, UC_MODE_32)
cs = Cs(CS_ARCH_X86, CS_MODE_32)
cs.detail = True

uc.mem_map(IMG_BASE, IMG_SIZE)
uc.mem_map(STACK_BASE, STACK_SIZE)

uc.mem_write(IMG_BASE, shellcode)
uc.reg_write(UC_X86_REG_ESP, STACK_BASE + STACK_SIZE // 2)

def telescope_stack_args(uc, no_args, telescope_len=20):
    r_esp = uc.reg_read(UC_X86_REG_ESP)
    for i in range(no_args):
        arg_val = u32(uc.mem_read(r_esp + i * 4, 4))
        print(f'    arg[{i}]={hex(arg_val)}', end='')
        # only check start of data, will throw if ends out of range
        if  IMG_BASE <= arg_val <= IMG_BASE + IMG_SIZE or \
            STACK_BASE <= arg_val <= STACK_BASE + STACK_SIZE:
            telescope = uc.mem_read(arg_val, telescope_len)
            print(f'->{telescope}')
        else:
            print('')

def hook_mem_valid_access(uc, access_type, address, size, value, user_data):
    if access_type == UC_MEM_READ:
        print('    UC_MEM_READ', end='')
    elif access_type == UC_MEM_WRITE:
        print('    UC_MEM_WRITE', end='')
    elif access_type == UC_MEM_FETCH:
        print('    UC_MEM_FETCH', end='')
    print(f' -> [{hex(address)}] = {hex(value)} ({size})')

def hook_mem_invalid_access(uc, access_type, address, size, value, user_data):
    if access_type == UC_MEM_READ_UNMAPPED:
        print('    UC_MEM_READ_UNMAPPED', end='')
    elif access_type == UC_MEM_WRITE_UNMAPPED:
        print('    UC_MEM_WRITE_UNMAPPED', end='')
        # We can uc.mem_map() accessed memory and return True to continue execution
    elif access_type == UC_MEM_FETCH_UNMAPPED:
        print('    UC_MEM_FETCH_UNMAPPED', end='')
    elif access_type == UC_MEM_WRITE_PROT:
        print('    UC_MEM_WRITE_PROT', end='')
    elif access_type == UC_MEM_READ_PROT:
        print('    UC_MEM_READ_PROT', end='')
    elif access_type == UC_MEM_FETCH_PROT:
        print('    UC_MEM_FETCH_PROT', end='')
    print(f' -> [{hex(address)}] = {hex(value)} ({size})')

    # return False to indicate we want to stop emulation
    # lol it looks like iot does not work
    return False

def hook_instruction(uc, address, size, user_data): 
    machine_code = uc.mem_read(address, size)
    for i in cs.disasm(machine_code, address):
        print("0x{:08x}: {} {} {}".format(
            i.address, 
            ' '.join(['{:02x}'.format(b) for b in i.bytes]).ljust(20),
            i.mnemonic,
            i.op_str))
    
    # afaik - we can't hook calls in capstone, need to do it manually
    instr = next(cs.disasm(machine_code, address))
    if instr.mnemonic == 'call':
        # "print" call arguments
        telescope_stack_args(uc, 3);

        op = i.operands[0]
        if op.type == X86_OP_IMM:
            if IMG_BASE <= op.value.imm <= IMG_BASE + IMG_SIZE:
                # execute call if dest in image address range
                return
        # skip call if dest out of image address range or indirect call
        uc.reg_write(UC_X86_REG_EIP, address + size)


# hook instructions
uc.hook_add(UC_HOOK_CODE, hook_instruction)
uc.hook_add(UC_HOOK_MEM_VALID, hook_mem_valid_access)
uc.hook_add(UC_HOOK_MEM_INVALID, hook_mem_invalid_access)

#TODO: hooking mem https://github.com/unicorn-engine/unicorn/blob/3cea38bff7bf0986337ef0fbf979f2afda42b9fc/bindings/python/unicorn/unicorn.py#L517

uc.emu_start(IMG_BASE, IMG_BASE - 1)
