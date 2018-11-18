def str2num(s):
    s = bytearray(s)  # So I don't have to call ord() all the time.
    n = 0
    for v in s:
	n *= 0x100
	n += v
    return n


def num2str(n):
    o = []
    while n != 0:
	o.append(chr(n % 0x100))  # n & 0xff would work too
	n /= 0x100 # n >>= 8 would work too
    return ''.join(o)[::-1]


def str2num_hack(s):
    return int(s.encode("hex"), 16)


def num2str_hack(n):
    return hex(n).replace("L", "")[2:].decode("hex")


text = "Hello World"

enc_test1 = str2num(text)
dec_test1 = num2str(enc_test1)

enc_test2 = str2num_hack(text)
dec_test2 = num2str_hack(enc_test2)

print "Text:", text

print "Method 1 (encode):", enc_test1
print "Method 1 (decode):", dec_test1

print "Method 2 (encode):", enc_test2
print "Method 2 (decode):", dec_test2

