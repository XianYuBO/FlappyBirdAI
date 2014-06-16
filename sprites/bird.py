import cocos
import cocos.collision_model
import cocos.euclid
import pyglet

import setting


class Bird(cocos.sprite.Sprite):

    def __init__(self):
        position = (setting.GAME_WIDTH * 0.3, setting.GAME_HEIGHT / 2)
        self.init_position = position
        self.bird_images = pyglet.image.ImageGrid(pyglet.resource.image("resources/bird.png"), 1, 3)
        self.bird_animation = pyglet.image.Animation.from_image_sequence(self.bird_images, 0.1, loop=True)
        self.cshape = cocos.collision_model.AARectShape(cocos.euclid.Vector2(*position),
                                                        self.bird_images[0].width / 2, self.bird_images[0].height / 2)
        self.jump_action = None
        self.down_action = None
        self.crash_action = None
        super(Bird, self).__init__(image=self.bird_animation, position=position)

    def reset(self):
        self.position = self.init_position
        self.rotation = 0
        self.stop()
        self.jump_action = None
        self.down_action = None
        self.crash_action = None
        self.image = self.bird_animation

    def update_cshape(self):
        self.cshape = cocos.collision_model.AARectShape(cocos.euclid.Vector2(*self.position),
                                                        self.bird_images[0].width / 2, self.bird_images[0].height / 2)

    def cancel_jump(self):
        if self.jump_action is not None and not self.jump_action.done():
            self.remove_action(self.jump_action)
            self.jump_action = None

    def cancel_down(self):
        if self.down_action is not None and not self.down_action.done():
            self.remove_action(self.down_action)
            self.down_action = None

    def top_collision(self):
        self.cancel_jump()

    def other_collision(self):
        self.image = self.bird_images[0]
        self.cancel_jump()
        self.cancel_down()
        self.crash()

    def jump(self):
        self.cancel_down()
        self.cancel_jump()
        self.jump_action = self.do(
            cocos.actions.Reverse(
                cocos.actions.Accelerate(
                    cocos.actions.MoveBy((0, -50), duration=0.3)))
            |
            cocos.actions.RotateTo(-35, 0.2)
        )

    def crash(self):
        if self.crash_action is None:
            self.rotation = 90
            self.crash_action = self.do(cocos.actions.Repeat(
                cocos.actions.MoveBy((0, -50), duration=0.1)))

    def down(self):
        if not self.are_actions_running():
            self.down_action = self.do(
                (cocos.actions.Accelerate(
                    cocos.actions.MoveBy((0, -50), duration=0.2))
                 +
                 cocos.actions.Repeat(
                     cocos.actions.MoveBy((0, -50), duration=0.1)))
                |
                cocos.actions.RotateTo(90, 0.4))
