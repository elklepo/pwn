class Wall2x2(object):
    def __init__(self, color):
        self.tl = color  # top left
        self.tr = color  # top right
        self.bl = color  # bottom left
        self.br = color  # bottom right

    def get_all(self):
        return self.tl, self.tr, self.bl, self.br

    def get_left(self):
        return self.tl, self.bl

    def get_right(self):
        return self.tr, self.br

    def get_top(self):
        return self.tl, self.tr

    def get_bottom(self):
        return self.bl, self.br

    def set_left(self, left):
        self.tl, self.bl = left

    def set_right(self, right):
        self.tr, self.br = right

    def set_top(self, top):
        self.tl, self.tr = top

    def set_bottom(self, bottom):
        self.bl, self.br = bottom

    def clockwise(self):
        self.tl, self.tr, \
        self.bl, self.br = self.bl, self.tl, \
                           self.br, self.tr

    def counterclockwise(self):
        self.clockwise()
        self.clockwise()
        self.clockwise()

    def is_completed(self):
        return self.tl == self.tr == \
               self.bl == self.br
