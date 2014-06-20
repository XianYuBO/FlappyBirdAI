count = -1


def controller(environment):
    global count
    count += 1
    if environment["game_over"]:
        return "reset"
    up_tube, down_tube = get_nearest_tube_pair(environment)
    if environment["bird"].center.y - environment["bird"].ry < down_tube.center.y + down_tube.ry + 25 and not environment["jumping"]:
        return "jump"


def get_nearest_tube_pair(environment):
    tmp = filter(lambda (up_tube, down_tube, status):
                 up_tube.center.x + up_tube.rx > environment["bird"].center.x - environment["bird"].rx,
                 environment["tubes"])
    tmp1 = map(lambda (x, y, z): (x, y), tmp)
    return min(tmp1, key=lambda (x, y): x.center.x + x.rx - (environment["bird"].center.x - environment["bird"].rx))

