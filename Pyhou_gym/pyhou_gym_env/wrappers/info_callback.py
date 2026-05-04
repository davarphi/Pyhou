from stable_baselines3.common.callbacks import BaseCallback

class InfoCallback(BaseCallback):
    def _on_step(self):
        if self.locals["dones"][0]:
            print(self.locals["infos"][0]["Enemy_health"])
            print(self.locals["infos"][0]["Bullets_shot"])
            print(self.locals["infos"][0]["Bullets_that_hit_player"])
            print(self.locals["infos"][0]["Bullets_that_hit_enemy"])
        return True