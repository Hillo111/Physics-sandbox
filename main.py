from shapes import *
from pixels import *
import pygame as pg
import numpy as np

shapes = [Circle(100, 100, 5, 0.5, 50, 0.01, (0, 0, 0), False, [0, 500, 0, 400])]

size = width, height = 500, 400

screen = pg.display.set_mode(size)
clock = pg.time.Clock()
run = True

last_pos = [0, 0]

while run:
    for e in pg.event.get():
        if e.type == pg.QUIT:
            run = False
        if e.type == pg.MOUSEBUTTONDOWN:
            new_pos = np.array(pg.mouse.get_pos())
            diff = new_pos - last_pos
            shape = Circle(new_pos[0], new_pos[1], 5, 0.5, 50, 0.01, (0, 0, 0), False, [0, 500, 0, 400])
            shape.vel_x, shape.vel_y = diff
            if shape.colliding(shapes) is None and not shape.hitting_wall():
                shapes.append(shape)

    last_pos = np.array(pg.mouse.get_pos())
    screen.fill((255, 255, 255))

    old_shapes = shapes.copy()
    for shape in old_shapes:
        shape.update(shapes)
    shapes = old_shapes

    for shape in shapes:
        shape.draw(screen)

    pg.display.flip()
    clock.tick(60)

pg.quit()