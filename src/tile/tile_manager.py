from random import shuffle
from tile.tile import Tile
from status.tile_type import TileType

TILE_NUM = 4


class TileManager:
    def __init__(self):
        self.tiles = []
        self.yama = []
        self.wanpai = []
        self.doras = []

    def _create(self):
        idx = 0
        for tile_type in TileType:
            all_num = 9 if tile_type is not TileType.JIHAI else 7
            for num in range(1, all_num + 1):
                for i in range(TILE_NUM):
                    self.tiles.append(Tile(idx, tile_type, num))
                    idx += 1
        shuffle(self.tiles)

    def reset(self):
        self._create()
        self.yama = self.tiles[:-14]
        self.wanpai = self.tiles[-14:]
        self.doras = [3]
        self.show()

    def haipai(self):
        ret = self.yama[:13]
        self.yama = self.yama[13:]
        return ret

    def tsumo(self):
        ret = self.yama[0]
        self.yama = self.yama[1:]
        return ret

    def show(self):
        # for tile in self.wanpai:
        #     print(tile)
        # doras = []
        # for i in self.doras:
        #     doras.append(self.wanpai[i])
        # print('dora: {}'.format(doras))
        print(len(self.tiles), len(self.yama), len(self.wanpai))

    def is_finish(self):
        return len(self.yama) == 0
