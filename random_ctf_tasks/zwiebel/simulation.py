#!/usr/bin/python3
#
# takes about 22 minutes on my machine to recover flag:
# hxp{1_h0p3_y0u_d1dnt_p33l_th3_0ni0n_by_h4nd}
#

from unicorn import *
from capstone import *
from capstone.x86 import *
from unicorn.x86_const import *


with open('./zwiebel', 'rb') as f:
    shellcode = f.read()[0x1310:0x25f9d]


BASE = 0x400000
STACK_ADDR = 0x0
STACK_SIZE = 1024*1024

uc = Uc(UC_ARCH_X86, UC_MODE_64)
cs = Cs(CS_ARCH_X86, CS_MODE_64)
cs.detail = True

uc.mem_map(BASE, 1024*1024)
uc.mem_map(STACK_ADDR, STACK_SIZE)

uc.mem_write(BASE, shellcode)
uc.reg_write(UC_X86_REG_ESP, STACK_ADDR + STACK_SIZE // 2)

flag = [0x20] * 100
offset = 0
mask = 0
def hook_instruction(uc, address, size, user_data):
    global offset
    global mask
    global flag
    machine_code = uc.mem_read(address, size)
    
    insn = next(cs.disasm(machine_code, address))
    if insn.mnemonic == 'je':
        uc.reg_write(UC_X86_REG_EIP, address + size)
        flag[offset] |= mask
        print('\r' + ''.join(map(chr, flag)), end='')
    
    if insn.mnemonic == 'jne':
        uc.reg_write(UC_X86_REG_EIP, address + size)
        flag[offset] &= (0xFF ^ mask)
        print('\r' + ''.join(map(chr, flag)), end='')
    
    if insn.mnemonic == 'mov':
        if 	insn.operands[0].type == X86_OP_REG and \
         	insn.operands[0].value.reg == UC_X86_REG_AL and \
         	insn.operands[1].type == X86_OP_MEM and \
         	insn.operands[1].value.mem.base == UC_X86_REG_RAX:
                offset = insn.operands[1].value.mem.disp

    if insn.mnemonic == 'and':
        if 	insn.operands[0].type == X86_OP_REG and \
        	insn.operands[0].value.reg == UC_X86_REG_AL and \
            insn.operands[1].type == X86_OP_IMM:
            	mask = insn.operands[1].value.imm

# hook other instructions
uc.hook_add(UC_HOOK_CODE, hook_instruction)
uc.emu_start(BASE, BASE - 1)
