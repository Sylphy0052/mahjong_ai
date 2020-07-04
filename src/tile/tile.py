from status.tile_type import TileType


JIHAI = ['東', '南', '西', '北', '白', '発', '中']


class Tile:
    def __init__(self, idx, tile_type, num):
        self.idx = idx
        self.tile_type = tile_type
        self.num = num
        if self.tile_type is TileType.JIHAI:
            self.char = JIHAI[self.num - 1]
        else:
            self.char = '{}{}'.format(self.num, self.tile_type.value)

    def __repr__(self):
        return self.char
