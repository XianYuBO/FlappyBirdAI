import sys
import importlib

import cocos

import layers.level
import setting


if __name__ == "__main__":
    if len(sys.argv) == 2:
        m = importlib.import_module(sys.argv[1])
        controller = m.controller
    else:
        controller = None
    cocos.director.director.init(width=setting.GAME_WIDTH, height=setting.GAME_HEIGHT)
    cocos.director.director.show_FPS = True
    layer = layers.level.Level(controller=controller)
    main_scene = cocos.scene.Scene(layer)
    cocos.director.director.run(main_scene)