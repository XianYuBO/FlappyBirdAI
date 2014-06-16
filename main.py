import cocos

import layers.level
import setting


if __name__ == "__main__":
    cocos.director.director.init(width=setting.GAME_WIDTH, height=setting.GAME_HEIGHT)
    cocos.director.director.show_FPS = True
    layer = layers.level.Level()
    main_scene = cocos.scene.Scene(layer)
    cocos.director.director.run(main_scene)