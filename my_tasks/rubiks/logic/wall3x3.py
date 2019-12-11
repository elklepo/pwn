class Wall3x3(object):
    def __init__(self, color):
        self.tl = color  # top left
        self.tm = color  # top middle
        self.tr = color  # top right
        self.ml = color  # middle left
        self.mm = color  # middle middle
        self.mr = color  # middle right
        self.bl = color  # bottom left
        self.bm = color  # bottom middle
        self.br = color  # bottom right

    def get_all(self):
        return self.tl, self.tm, self.tr, self.ml, self.mm, self.mr, self.bl, self.bm, self.br

    def get_left(self):
        return self.tl, self.ml, self.bl

    def get_right(self):
        return self.tr, self.mr, self.br

    def get_top(self):
        return self.tl, self.tm, self.tr

    def get_bottom(self):
        return self.bl, self.bm, self.br

    def set_left(self, left):
        self.tl, self.ml, self.bl = left

    def set_right(self, right):
        self.tr, self.mr, self.br = right

    def set_top(self, top):
        self.tl, self.tm, self.tr = top

    def set_bottom(self, bottom):
        self.bl, self.bm, self.br = bottom

    def clockwise(self):
        self.tl, self.tm, self.tr, \
        self.ml,          self.mr, \
        self.bl, self.bm, self.br = self.bl, self.ml, self.tl, \
                                    self.bm,          self.tm, \
                                    self.br, self.mr, self.tr

    def counterclockwise(self):
        self.clockwise()
        self.clockwise()
        self.clockwise()

    def is_completed(self):
        return self.tl == self.tm == self.tr == \
               self.ml == self.mm == self.mr == \
               self.bl == self.bm == self.br
