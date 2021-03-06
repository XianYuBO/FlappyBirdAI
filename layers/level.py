#-*- coding:utf-8 -*-
import pyglet
import cocos
import cocos.collision_model
import cocos.euclid

import setting
import sprites.bird
import sprites.tubes
import sprites.ground


class Level(cocos.layer.Layer):

    is_event_handler = True

    def __init__(self, controller=None):
        super(Level, self).__init__()
        if controller is None:
            self.controller = None
        else:
            self.is_event_handler = False
            self.controller = controller
        self.game_over = False
        self.already_set_game_over = False
        self.resetting = False
        self.time_delta = 0

        self.score = 0
        self.score_label = cocos.text.Label('0', font_name='Times New Roman',
                                            font_size=24, anchor_x='center', anchor_y='center',
                                            multiline=True, width=setting.GAME_WIDTH, align='center')
        self.score_label.position = setting.GAME_WIDTH / 2, setting.GAME_HEIGHT * 0.8
        self.add(self.score_label, z=3)

        background = cocos.sprite.Sprite("resources/bg.png")
        background.position = (setting.GAME_WIDTH / 2, setting.GAME_HEIGHT / 2)
        self.add(background, z=0)

        self.tubes = sprites.tubes.Tubes(3)
        for up_tube, down_tube, _ in self.tubes.tube_lst:
            self.add(up_tube, z=1)
            self.add(down_tube, z=1)

        self.ground = sprites.ground.Ground(setting.GROUND_Y)
        self.add(self.ground, z=1)

        self.sky = sprites.ground.Ground(setting.SKY_Y)
        self.sky.visible = False
        self.add(self.sky, z=1)

        self.bird = sprites.bird.Bird()
        self.add(self.bird, z=2)

        self.other_collision_manager = cocos.collision_model.CollisionManagerBruteForce()
        self.top_collision_manager = cocos.collision_model.CollisionManagerBruteForce()
        self.top_collision_manager.add(self.sky)

        self.schedule(self.update)

    def reset(self):
        self.score = 0
        self.score_label.element.text = '0'
        self.tubes.reset()
        self.bird.reset()
        self.ground.resume()
        self.ground.resume()
        self.game_over = False
        self.resetting = False
        self.already_set_game_over = False
        self.time_delta = 0

    def on_key_press(self, symbol, modifiers):
        if not self.game_over and symbol == pyglet.window.key.SPACE:
            self.bird.jump()
        if self.game_over and symbol == pyglet.window.key.R:
            self.reset()

    def update_score(self):
        for tube_pair in self.tubes.tube_lst:
            up_tube, _, bird_pass_status = tube_pair
            if not bird_pass_status:
                if self.bird.x > up_tube.x + up_tube.width / 2:
                    self.score += 1
                    tube_pair[-1] = True
                    self.score_label.element.text = str(self.score)

    def get_environment(self):
        return {
            "game_over": self.game_over,
            "score": self.score,
            "tubes": map(lambda (up, down, status): (up.cshape, down.cshape, status), self.tubes.tube_lst),
            "bird": self.bird.cshape,
            "jumping": True if self.bird.jump_action is not None and not self.bird.jump_action.done() else False
        }

    def ai_controller(self, dt):
        if self.controller is not None:
            r = self.controller(self.get_environment())
            if not self.game_over and r == "jump":
                self.bird.jump()
            elif r == "reset" and self.game_over and not self.resetting:
                self.resetting = True
                self.time_delta = 0
            elif self.game_over and self.resetting:
                if self.time_delta > 1.5:
                    self.reset()
                else:
                    self.time_delta += dt

    def update(self, dt):
        self.ai_controller(dt)

        if self.already_set_game_over:
            return
        if self.game_over:
            self.score_label.element.text = "Game Over\npress R restart\ntotal score:%s" % self.score
            self.ground.pause()
            self.tubes.pause()
            self.sky.pause()
            self.bird.other_collision()
            self.already_set_game_over = True
            return

        self.tubes.update(dt)
        self.update_score()
        self.bird.down()

        self.other_collision_manager.clear()

        self.bird.update_cshape()
        self.sky.update_cshape()
        self.ground.update_cshape()
        self.tubes.update_cshape()

        for up_tube, down_tube, _ in self.tubes.tube_lst:
            self.other_collision_manager.add(up_tube)
            self.other_collision_manager.add(down_tube)
        self.other_collision_manager.add(self.ground)
        if self.other_collision_manager.objs_colliding(self.bird):
            self.game_over = True
        if self.top_collision_manager.objs_colliding(self.bird):
            self.bird.top_collision()
