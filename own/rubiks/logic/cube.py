import os
import sys


class Cube(object):
    def __init__(self, wall_type, fmt):
        self.f = wall_type('r')
        self.b = wall_type('o')
        self.u = wall_type('b')
        self.d = wall_type('g')
        self.l = wall_type('w')
        self.r = wall_type('y')
        self.fmt = fmt

    def up_clockwise(self):
        self.u.clockwise()
        f = self.f.get_top()
        r = self.r.get_top()
        b = self.b.get_top()
        l = self.l.get_top()
        self.f.set_top(r)
        self.r.set_top(b)
        self.b.set_top(l)
        self.l.set_top(f)

    def up_counterclockwise(self):
        self.up_clockwise()
        self.up_clockwise()
        self.up_clockwise()

    def bottom_clockwise(self):
        self.d.clockwise()
        f = self.f.get_bottom()
        r = self.r.get_bottom()
        b = self.b.get_bottom()
        l = self.l.get_bottom()
        self.f.set_bottom(l)
        self.r.set_bottom(f)
        self.b.set_bottom(r)
        self.l.set_bottom(b)

    def bottom_counterclockwise(self):
        self.bottom_clockwise()
        self.bottom_clockwise()
        self.bottom_clockwise()

    def left_clockwise(self):
        self.l.clockwise()
        f = self.f.get_left()
        b = self.d.get_left()
        d = self.b.get_right()
        u = self.u.get_left()
        self.f.set_left(u)
        self.d.set_left(f)
        self.b.set_right(b[::-1])
        self.u.set_left(d[::-1])

    def left_counterclockwise(self):
        self.left_clockwise()
        self.left_clockwise()
        self.left_clockwise()

    def right_clockwise(self):
        self.r.clockwise()
        f = self.f.get_right()
        b = self.b.get_left()
        d = self.d.get_right()
        u = self.u.get_right()
        self.f.set_right(d)
        self.b.set_left(u[::-1])
        self.d.set_right(b[::-1])
        self.u.set_right(f)

    def right_counterclockwise(self):
        self.right_clockwise()
        self.right_clockwise()
        self.right_clockwise()

    def front_clockwise(self):
        self.f.clockwise()
        u = self.u.get_bottom()
        l = self.l.get_right()
        d = self.d.get_top()
        r = self.r.get_left()
        self.u.set_bottom(l[::-1])
        self.l.set_right(d)
        self.d.set_top(r[::-1])
        self.r.set_left(u)

    def front_counterclockwise(self):
        self.front_clockwise()
        self.front_clockwise()
        self.front_clockwise()

    def back_clockwise(self):
        self.b.clockwise()
        u = self.u.get_top()
        l = self.l.get_left()
        d = self.d.get_bottom()
        r = self.r.get_right()
        self.u.set_top(r)
        self.l.set_left(u[::-1])
        self.d.set_bottom(l)
        self.r.set_right(d[::-1])

    def back_counterclockwise(self):
        self.back_clockwise()
        self.back_clockwise()
        self.back_clockwise()

    def turn_left(self):
        self.f, self.l, self.b, self.r = self.r, self.f, self.l, self.b
        self.u.clockwise()
        self.d.counterclockwise()

    def turn_right(self):
        self.turn_left()
        self.turn_left()
        self.turn_left()

    def turn_down(self):
        self.f, self.d, self.b, self.u = self.u, self.f, self.d, self.b
        self.u.clockwise()
        self.u.clockwise()
        self.b.clockwise()
        self.b.clockwise()
        self.l.clockwise()
        self.r.counterclockwise()

    def turn_up(self):
        self.turn_down()
        self.turn_down()
        self.turn_down()

    def is_completed(self):
        return self.u.is_completed() and \
               self.d.is_completed() and \
               self.l.is_completed() and \
               self.r.is_completed() and \
               self.b.is_completed() and \
               self.f.is_completed()

    def shuffle(self, rounds=1000):
        methods = [self.up_clockwise, self.up_counterclockwise, self.bottom_counterclockwise, self.bottom_clockwise,
                   self.right_clockwise, self.right_counterclockwise, self.left_counterclockwise, self.left_counterclockwise,
                   self.front_clockwise, self.front_counterclockwise, self.back_counterclockwise, self.back_counterclockwise]
        rand_byte_array = os.urandom(rounds)
        # regression check for , check if corners have three different colors
        for b in rand_byte_array:
            methods[ord(b) % len(methods)]()
            if self.f.tl == self.u.bl or self.u.bl == self.l.tr or self.l.tr == self.f.tl:
                print >> sys.stderr, 'FTL corner error: ' + methods[ord(b) % len(methods)].__name__
                exit(0)
            if self.u.tl == self.l.tl or self.l.tl == self.b.tr or self.b.tr == self.u.tl:
                print >> sys.stderr, 'TLE corner error: ' + methods[ord(b) % len(methods)].__name__
                exit(0)
            if self.b.br == self.l.bl or self.l.bl == self.d.bl or self.d.bl == self.b.br:
                print >> sys.stderr, 'ELB corner error: ' + methods[ord(b) % len(methods)].__name__
                exit(0)
            if self.f.bl == self.d.tl or self.d.tl == self.l.br or self.l.br == self.f.bl:
                print >> sys.stderr, 'BLF corner error: ' + methods[ord(b) % len(methods)].__name__
                exit(0)
            if self.f.tr == self.u.br or self.u.br == self.r.tl or self.r.tl == self.f.tr:
                print >> sys.stderr, 'FTR corner error: ' + methods[ord(b) % len(methods)].__name__
                exit(0)
            if self.u.tr == self.r.tr or self.r.tr == self.b.tl or self.b.tl == self.u.tr:
                print >> sys.stderr, 'TRE corner error: ' + methods[ord(b) % len(methods)].__name__
                exit(0)
            if self.b.bl == self.r.br or self.r.br == self.d.br or self.d.br == self.b.bl:
                print >> sys.stderr, 'ERB corner error: ' + methods[ord(b) % len(methods)].__name__
                break
            if self.f.br == self.d.tr or self.d.tr == self.r.bl or self.r.bl == self.f.br:
                print >> sys.stderr, 'BRF corner error: ' + methods[ord(b) % len(methods)].__name__
                exit(0)

    def __str__(self):
        term = {'r': '\033[31;41m', 'g': '\033[32;42m',  'y': '\033[93;103m',
                'b': '\033[34;44m', 'w': '\033[97;107m', 'o': '\033[33;43m', 'rst': '\033[0m'}
        fmt_args = list(self.u.get_all()) + list(self.l.get_all()) + list(self.f.get_all()) + \
                   list(self.r.get_all()) + list(self.b.get_all()) + list(self.d.get_all())
        fmt_args = ['{0}{1}{1}{1}{1}{2}'.format(term[f], f, term['rst']) for f in fmt_args]
        return self.fmt.format(*fmt_args)
