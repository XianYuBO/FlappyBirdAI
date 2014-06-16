import random
import math

import cocos
import cocos.collision_model
import cocos.euclid

import setting


class Tube(cocos.sprite.Sprite):

    def __init__(self, image_path, position):
        super(Tube, self).__init__(image=image_path, position=position)
        self.cshape = cocos.collision_model.AARectShape(cocos.euclid.Vector2(*position),
                                                        self.width / 2, self.height / 2)

    def update_cshape(self):
        self.cshape = cocos.collision_model.AARectShape(cocos.euclid.Vector2(*self.position),
                                                        self.width / 2, self.height / 2)


class Tubes(object):

    def __init__(self, num):
        self.tube_lst = []
        for i in xrange(1, num + 1):
            y1, y2 = self.get_tube_pair_y()
            x1 = x2 = setting.GAME_WIDTH + setting.TUBE_DURATION * i
            self.tube_lst.append([Tube("resources/tube1.png", (x1, y1)),
                                  Tube("resources/tube2.png", (x2, y2)),
                                  False])
        self.last_up_tube = self.tube_lst[-1][0]

    def reset(self):
        for i, tube_pair in enumerate(self.tube_lst):
            y1, y2 = self.get_tube_pair_y()
            x = setting.GAME_WIDTH + setting.TUBE_DURATION * (i + 1)
            tube_pair[0].position = (x, y1)
            tube_pair[1].position = (x, y2)
            tube_pair[2] = False
        self.last_up_tube = self.tube_lst[-1][0]

    def get_tube_pair_y(self):
        tmp = setting.GAME_HEIGHT / 2 + (random.random() - 0.5) * setting.GAME_HEIGHT * 0.2
        return setting.GAME_HEIGHT - math.floor(tmp - setting.OPENING / 2 - 320) - 160,\
               setting.GAME_HEIGHT - math.floor(tmp + setting.OPENING / 2) - 160

    def update_cshape(self):
        for up_tube, down_tube, _ in self.tube_lst:
            up_tube.update_cshape()
            down_tube.update_cshape()

    def pause(self):
        pass

    def update(self, dt):
        for tube_pair in self.tube_lst:
            up_tube, down_tube, count_status = tube_pair
            if up_tube.x + up_tube.width / 2 < 0 and down_tube.x + down_tube.width / 2 < 0:
                up_y, down_y = self.get_tube_pair_y()
                up_tube.x = down_tube.x = self.last_up_tube.x + setting.TUBE_DURATION
                up_tube.y = up_y
                down_tube.y = down_y
                self.last_up_tube = up_tube
                tube_pair[-1] = False
            else:
                up_tube.x -= dt * setting.SPEED
                down_tube.x -= dt * setting.SPEED

