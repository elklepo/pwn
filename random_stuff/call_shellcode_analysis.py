#!/usr/bin/python3
#
# CODE TAKEN FROM http://eternal.red/2018/unicorn-engine-tutorial/
# applied some modifications
#

from pwn import *
from unicorn import *
from capstone import *
from capstone.x86 import *
from unicorn.x86_const import *

with open('shellcode', 'rb') as f:
    shellcode = f.read()

BASE = 0x400000
STACK_ADDR = 0x0
STACK_SIZE = 1024*1024

uc = Uc(UC_ARCH_X86, UC_MODE_32)
cs = Cs(CS_ARCH_X86, CS_MODE_32)
cs.detail = True

uc.mem_map(BASE, 1024*1024)
uc.mem_map(STACK_ADDR, STACK_SIZE)

uc.mem_write(BASE, shellcode)
uc.reg_write(UC_X86_REG_ESP, STACK_ADDR + STACK_SIZE // 2)


def hook_instruction(uc, address, size, user_data): 
    machine_code = uc.mem_read(address, size)
    for i in cs.disasm(machine_code, address):
        print("0x{:08x}: {} {} {}".format(
            i.address, 
            ' '.join(['{:02x}'.format(b) for b in i.bytes]).ljust(20),
            i.mnemonic,
            i.op_str))
        for op in i.operands:
            if op.type == X86_OP_REG:
                print("\t\toperands[%u].type: REG = %s" %(1, i.reg_name(op.value.reg)))
            if op.type == X86_OP_MEM:
                print("\t\toperands[%u].type: MEM" %1)
                if op.value.mem.base != 0:
                    print("\t\t\toperands[%u].mem.base: REG = %s" \
                        %(1, i.reg_name(op.value.mem.base)))
                if op.value.mem.index != 0:
                    print("\t\t\toperands[%u].mem.index: REG = %s" \
                        %(1, i.reg_name(op.value.mem.index)))
                if op.value.mem.disp != 0:
                    print("\t\t\toperands[%u].mem.disp: 0x%x" \
                        %(1, op.value.mem.disp))
    
    instr = next(cs.disasm(machine_code, address))
    if instr.mnemonic == 'call':
        print 'call'

        
        r_esp = uc.reg_read(UC_X86_REG_ESP)
        print 'arg1', hex(u32(uc.mem_read(r_esp, 4)))
        print 'arg2', hex(u32(uc.mem_read(r_esp + 4, 4)))
        print 'arg3', hex(u32(uc.mem_read(r_esp + 8, 4)))
        uc.reg_write(UC_X86_REG_EIP, address + size)

# hook other instructions
uc.hook_add(UC_HOOK_CODE, hook_instruction)

#TODO: hooking mem https://github.com/unicorn-engine/unicorn/blob/3cea38bff7bf0986337ef0fbf979f2afda42b9fc/bindings/python/unicorn/unicorn.py#L517

uc.emu_start(BASE, BASE - 1)
