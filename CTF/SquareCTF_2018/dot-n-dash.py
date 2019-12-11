import sys
import collections


def read_and_recover_numbers():
    with open(r"./_dot-n-dash/instructions.txt") as f:
        l = list()
        count = 0
        while True:
            c = f.read(1)
            if not c:
                f.close()
                break
            if c == '-':
                count += 1
            if c == '.':
                l.append(count)
                count = 0
    return l


def parse(n):
    c_pos = (n - 1) >> 3
    b_pos = (n - 1) & 0x7
    return c_pos, b_pos


if __name__ == '__main__':
    nums = read_and_recover_numbers()
    d = dict()
    for num in nums:
        char_pos, bit_pos = parse(num)
        if char_pos in d:
            d[char_pos] |= 1 << bit_pos
        else:
            d[char_pos] = 1 << bit_pos

    sort_d = collections.OrderedDict(sorted(d.items(), reverse=True))
    for k, v in sort_d.items(): #  iteritems() for Python 2.x
        sys.stdout.write(chr(v))
    sys.stdout.flush()

