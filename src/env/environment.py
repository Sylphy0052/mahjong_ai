from env.field import Field
from agent.player_manager import PlayerManager


class Environment:
    def __init__(self):
        field = Field()
        self.player_mgr = PlayerManager(field)

    def run(self):
        # 何局か
        while True:
            # 1局
            self.player_mgr.first()
            while True:
                # 1Turn
                flg = self.player_mgr.action()
                if flg:
                    break
            break
