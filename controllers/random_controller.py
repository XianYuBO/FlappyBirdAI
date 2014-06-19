import random


def controller(environment):
    if environment["score"] > 0:
        print "yes!!!!!!"
    r = random.random()
    if environment["game_over"]:
        return "reset"
    if r < 0.08:
        return "jump"
