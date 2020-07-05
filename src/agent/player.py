from tile.judge_yaku import judge_shanten
from status.yaku_type import YakuType


class Player:
    def __init__(self, idx):
        self.idx = idx
        self.tehai = []
        self.misehai = []
        self.sutehai = []
        self.jikaze = None
        self.is_richi = False

    def set_jikaze(self, kaze):
        self.jikaze = kaze

    def reset(self):
        self.tehai = []

    def haipai(self, tiles):
        self.tehai = tiles
        self.tehai = sorted(self.tehai, key=lambda t: t.idx)

    def tsumo(self, tile):
        self.tehai.append(tile)
        # FOR DEBUG
        judge_shanten(self.tehai, self.misehai)

    def sute(self):
        tile = self.tehai[-1]
        self.sutehai.append(tile)
        self.tehai.remove(tile)
        return tile

    def chi(self, tile):
        pass

    def pon(self, tile):
        pass

    def kan(self, tile):
        pass

    def ankan(self):
        pass

    def ron(self, tile):
        pass

    def is_naki(self, tile):
        return False

    def is_ron(self, tile):
        pass

    def is_tsumo(self):
        pass

    def __repr__(self):
        return 'Player{} kaze: {} \ntehai: {} {} \nsutehai {}'.format(self.idx, self.jikaze, self.tehai, self.misehai, self.sutehai)
