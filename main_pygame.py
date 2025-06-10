
"""

"""

import P as P
P.MPL0PYGAME1 = 1
import pygame

import numpy as np
import random
random.seed(3)  # ONLY HERE
np.random.seed(3)  # ONLY HERE
import time

from src.gen_objects import GenObjects
from src.load_pics import load_pics
from src.genesis import _genesis
from src.a_pygame.draw_helpers_pygame import *
from src.a_pygame.write_to_file import VideoWriter
from src.logger import Logger

g = GenObjects()
g.pics = load_pics()
g.gis = _genesis()

o0calidus = g.gen_calidus()
g.gen_planets_moons(o0calidus)

if 'Rockets' in P.OBJ_TO_SHOW:
    R = g.gen_rockets(o0calidus)
else:
    R = None

_logger = Logger(o0calidus, R)

print("Done prep =============================\n")
'''PYGAME INIT =============================================='''
pygame.init()
# flags = pygame.HWSURFACE | pygame.DOUBLEBUF
# flags = pygame.HWSURFACE | pygame.DOUBLEBUF | pygame.RESIZABLE #| pygame.FULLSCREEN  # dont seem to be needed
# screen = pygame.display.set_mode((P.MAP_DIMS[0], P.MAP_DIMS[1]), flags=flags)
screen = pygame.display.set_mode((P.MAP_DIMS[0], P.MAP_DIMS[1]))

backgr_surf = gen_backgr(g.pics)

if P.WRITE:
    vw = VideoWriter('./vids/vid_' + str(P.WRITE) + '_' + P.VID_SINGLE_WORD + '_' + '.mp4', P.MAP_DIMS, P.FPS)

D = []

print("Done prep =============================\n")  # OBS D is always empty here
'''ANIMATION LOOP ==========================================='''

clock = pygame.time.Clock()
time0 = time.perf_counter()
i = 0
running = True
while running:

    # If ESC pressed then quit =============
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

    screen.blit(backgr_surf, (0, 0))  #

    # =======================================
    D = []  # Drawables (objects shown in the animation): Rebuilt each iteration!
    for o1_id, o1 in o0calidus.O1.items():
        if i == o1.frame_ss[0]:
            o1.start_draw(D)  # creates surfaces and rects
        elif i > o1.frame_ss[0] and i < o1.frame_ss[1]:
            o1.age += 1
            o1.update_draw(D)
        elif i >= o1.frame_ss[1]:
            pass

    if 'Rockets' in P.OBJ_TO_SHOW:
        for rocket in R:
            if i == rocket.frame_ss[0]:
                rocket.update_draw(D)
            elif i > rocket.frame_ss[0] and i < rocket.frame_ss[1]:
                rocket.age += 1
                rocket.update_draw(D)
            elif i == rocket.frame_ss[1]:
                pass

    for _, type, tuple in sorted(D, key=lambda x:x[0]):
        if type == 'rocket':
            color = (tuple[0], tuple[0], tuple[0])
            pos = tuple[1]
            r = tuple[2]
            alpha = tuple[3]

            if alpha < 255:
                surface = pygame.Surface((r * 2, r * 2), pygame.SRCALPHA)
                pygame.draw.circle(surface, color + (alpha,), (r, r), r)
                screen.blit(surface, (pos[0] - r, pos[1] - r))
            else:
                pygame.draw.circle(screen, color, pos, r)
        else:
            screen.blit(tuple[0], tuple[1])

    # =======================
    if P.WRITE:
        vw.write_frame(screen)
    else:
        pygame.display.flip()

    pygame.display.flip()
    clock.tick(P.FPS)
    i += 1

    if i % 100 == 0:
        print(i)

    if i == P.FRAMES_STOP - 1:
        print("DONE LOOP ==========================================================")
        break

time1 = time.perf_counter() - time0

min_vid = ((P.FRAMES_STOP - P.FRAMES_START) / P.FPS) / 60
sec_per_1_min = int(time1 / min_vid)
print("sec_per_1_min: " + str(sec_per_1_min))

_logger.row[9] = int(sec_per_1_min)

if P.WRITE:
    vw.close()

_logger.get_ram_usage_mb()
if P.SAVE == 1:
    _logger.add_save()

pygame.quit()
