FlappyBirdAI
============

- Write the AI of the Flappy Bird: both machine learning methods and rule-based methods are permitted.
- All codes are written by pure python.

Dependences
============
- python 2.7.5
- pyglet
- cocos2d

Install dependences
============
- `pip install pyglet`
- `pip install cocos2d`

How to run this project
============
- `python main.py` - human can control this game, *key space* makes the bird jump, *key r* makes the game restart.
- `python main.py controllers.xxxxx` - AI controls this game. For example: `python main.py controllers.simple_controller`

How to write AI
============
Do it as the random_controller does.

- the game will call your controller's controller function, and give you the environment's data(
if you want know more information about environment's data, you can see it in level.py).
- Based on environment's data, you can return 'jump' which makes the bird jump, or return 'reset' which makes the game
restart.Returning nothing is permitted, which means that you don't change the bird's status at current frame.


Others
============
All pictures are from [flappy](https://github.com/hyspace/flappy)

