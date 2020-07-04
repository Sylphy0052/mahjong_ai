class Player:
    def __init__(self, idx):
        self.idx = idx
        self.tehai = []
        self.sutehai = []
        self.jikaze = None

    def set_jikaze(self, kaze):
        self.jikaze = kaze

    def reset(self):
        self.tehai = []

    def haipai(self, tiles):
        self.tehai = tiles
        self.tehai = sorted(self.tehai, key=lambda t: t.idx)

    def tsumo(self, tile):
        self.tehai.append(tile)

    def sute(self):
        tile = self.tehai[-1]
        self.sutehai.append(tile)
        self.tehai.remove(tile)

    def __repr__(self):
        return 'Player{} kaze: {} tehai: {}'.format(self.idx, self.jikaze, self.tehai)
