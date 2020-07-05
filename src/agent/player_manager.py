from random import shuffle
from agent.player import Player


KAZE = ['東', '南', '西', '北']


class PlayerManager:
    def __init__(self, field):
        self.field = field
        self.players = []
        # for i in range(1, 5):
        for i in range(1, 2):
            self.players.append(Player(i))
        shuffle(self.players)
        for i, player in enumerate(self.players):
            player.set_jikaze(KAZE[i])

    def action(self):
        for player in self.players:
            tile = self.field.tsumo()
            player.tsumo(tile)
            tile = player.sute()
            print(player)
            if self.field.is_finish():
                return True
        return False

    def first(self):
        self.field.reset()
        for player in self.players:
            player.reset()

        for player in self.players:
            player.haipai(self.field.get_tile_mgr().haipai())
        self.show()

    def next(self):
        player = self.players[0]
        self.players.remove(player)
        self.players.append(player)

    def show(self):
        for player in self.players:
            print(player)
