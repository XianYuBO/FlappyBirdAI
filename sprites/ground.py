import cocos
import cocos.euclid
import cocos.collision_model

import setting


class Ground(cocos.sprite.Sprite):

    def __init__(self, y):
        super(Ground, self).__init__(image="resources/ground.png")
        position = (setting.GAME_WIDTH - self.width / 2, y)
        self.position = position
        self.cshape = cocos.collision_model.AARectShape(cocos.euclid.Vector2(*position),
                                                        self.width / 2, self.height / 2)
        ground_action = cocos.actions.Repeat(
            cocos.actions.MoveTo((setting.GAME_WIDTH / 2, y),
                                 duration=(self.width - setting.GAME_WIDTH) / 2.0 / setting.SPEED)
            +
            cocos.actions.Place((setting.GAME_WIDTH - self.width / 2, y))
        )
        self.do(ground_action)

    def update_cshape(self):
        pass
