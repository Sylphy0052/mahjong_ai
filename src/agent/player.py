from tile.judge_yaku import judge_shanten, get_comb, get_primary, get_iso
from status.yaku_type import YakuType
# from time import time


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
        print('自摸: {}'.format(tile))

    def sute(self):
        # start_time = time()
        # ここに孤立牌を捨てるプログラムを入れる
        iso_tiles = get_iso(self.tehai)
        print('孤立牌 {}'.format(iso_tiles))
        if len(iso_tiles) > 0:
            tile = iso_tiles[-1]
            tile_idx = tile.idx
        else:
            comb_tiles, iso_tiles = get_comb(self.tehai)
            if len(iso_tiles) == 0:
                comb = get_primary(comb_tiles)
                if comb is None:
                    shanten = judge_shanten(self.tehai, self.misehai)
                    print(shanten)
                    raise Exception
                tile = comb[-1]
                tile_idx = tile.idx
            else:
                tile = iso_tiles[-1]
                tile_idx = tile.idx
        print('捨て {}'.format(tile))
        self.sutehai.append(tile)
        for i, t in enumerate(self.tehai):
            if t.idx == tile_idx:
                del self.tehai[i]
        # self.tehai.remove(tile)
        self.tehai = sorted(self.tehai, key=lambda t: t.idx)
        # print('Time: {:.1f}'.format(time() - start_time))
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
