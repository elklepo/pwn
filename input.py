from pwn import*
import os

port = 9977
a=[str(v) for v in range(0, 100)]
a[0] = './input'
a[ord('A')] = ''
a[ord('B')] = '\x20\x0a\x0d'
a[ord('C')] = str(port)


def pwntools_style():
    r0, w0 = os.pipe()
    r1, w1 = os.pipe()
    os.write(w0, "\x00\x0a\x00\xff")
    os.write(w1, "\x00\x0a\x02\xff")

    with open("\x0a", "w") as f:
        f.write("\x00\x00\x00\x00")    

    p = process(a, stdin=r0, stderr=r1, env={"\xde\xad\xbe\xef" : "\xca\xfe\xba\xbe"})
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    r = remote('localhost', port)
    r.send("\xde\xad\xbe\xef")
    p.wait()
    print p.recv(4096, timeout=1)


def classic():
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
        os.execv('./input', a)
    else:
        os.close(r0)
        os.close(r2)
        os.write(w0, '\x00\x0a\x00\xff')
        os.write(w2, '\x00\x0a\x02\xff')
        os.close(w0)
        os.close(w2)
        r = remote('localhost', port)
        r.send('\xde\xad\xbe\xef')

