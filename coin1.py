from pwn import *
import time

def send_rcv(s_msg):
#    print '---->' + s_msg
    r.sendline(s_msg)
    r_msg = r.recvline()
#    print '<----' + r_msg
    return r_msg

def bin_search(start, end):
    middle = (start + end) // 2
    s_msg = ' '.join(map(str, range(start, middle + 1)))
    r_msg = send_rcv(s_msg)

    return (start, middle) if int(r_msg) % 10 != 0 else (middle + 1, end)


r = remote('localhost', 9007)
for i in range(100):
    start_line = r.recvline_startswith('N')

    spl = start_line.split(' ')
    chances = int(spl[1][2:])
    start = 0
    end = int(spl[0][2:]) - 1
#    print 'CHANCES: {}, START: {}, END: {}'.format(chances, start, end)

    for chance in range(chances):
        start, end = bin_search(start, end)

    r_msg = send_rcv(str(start))
    if not r_msg.startswith('Correct!'):
        print 'FAKAP'
        exit(1)

print r.recv() #  flag
r.close()

