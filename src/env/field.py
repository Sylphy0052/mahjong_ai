from tile.tile_manager import TileManager


class Field:
    def __init__(self):
        self.tile_mgr = TileManager()

    def reset(self):
        self.tile_mgr.reset()
        self.doras = [3]

    def tsumo(self):
        tile = self.tile_mgr.tsumo()
        return tile

    def is_finish(self):
        return self.tile_mgr.is_finish()

    def get_tile_mgr(self):
        return self.tile_mgr
