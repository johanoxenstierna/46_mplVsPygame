"""

"""

import P as P
P.MPL0PYGAME1 = 0

import numpy as np
import random
random.seed(3)  # ONLY HERE
np.random.seed(3)  # ONLY HERE
import time
import pickle

import matplotlib.animation as animation
from src.gen_objects import GenObjects
from src.load_pics import load_pics
from src.genesis import _genesis
from src.a_mpl.draw_helpers_mpl import *
from src.logger import Logger

Writer = animation.writers['ffmpeg']
writer = Writer(fps=P.FPS, bitrate=3600)  #, extra_args=['-vcodec', 'h264_nvenc'])

# if P.WRITE != 0:
#     # fig, ax_b = plt.subplots(figsize=(19.2, 10.8), dpi=100)
#     # fig = plt.figure(figsize=(12.8, 7.2), dpi=100)

# else:
    # fig, ax_b = plt.subplots(figsize=(19.2, 10.8), dpi=100)
    # fig, ax_b = plt.subplots(figsize=(19.2, 10.8))
    # fig = plt.figure(figsize=(16, 9), dpi=1920/16)
    # fig = plt.figure(figsize=(12.8, 7.2), dpi=100)
    # fig = plt.figure(figsize=(10, 6))

fig = plt.figure(figsize=(P.MAP_DIMS[0] / 100, P.MAP_DIMS[1] / 100), dpi=100)
ax_b = plt.gca()

fig.subplots_adjust(bottom=0)
fig.subplots_adjust(top=1)
fig.subplots_adjust(right=1)
fig.subplots_adjust(left=0)

g = GenObjects()
g.pics = load_pics()
g.gis = _genesis()
# g.real_scale()
gen_backgr(g.pics, ax_b)
o0calidus = g.gen_calidus()
g.gen_planets_moons(o0calidus)

if 'Rockets' in P.OBJ_TO_SHOW:
    R = g.gen_rockets(o0calidus)
else:
    R = None

# with open('./vids/gis', 'wb') as f:
#     pickle.dump(g.gis, f)

_logger = Logger(o0calidus, R)

D = []

# for o1_id, o1 in o0calidus.O1.items():
#     _ = o1.ani_update_step(ax_b, D)  # doesnt help

plt.gca().invert_yaxis()

print("Done prep =============================\n")  # OBS D is always empty here
'''ANIMATION LOOP ==========================================='''


def init():  # NEEDED FOR BLITTING
    return D #+ axs1


def animate(i):

    prints = "i: " + str(i) + "  len_axs0: " + str(len(D))

    # Artists that persist through whole animation ==============
    for o1_id, o1 in o0calidus.O1.items():
        if i == o1.frame_ss[0]:  # Assumes frames cannot be skipped.
            o1.start_draw(ax_b, D)
            o1.update_draw(ax_b)
        elif i > o1.frame_ss[0] and i < o1.frame_ss[1]:
            o1.age += 1
            o1.update_draw(ax_b)
        elif i >= o1.frame_ss[1]:
            pass  # No action bcs these objects persist through whole animation.

    # Artists that don't show all the time ========================
    if 'Rockets' in P.OBJ_TO_SHOW:
        for rocket in R:
            if i == rocket.frame_ss[0]:
                rocket.start_draw(ax_b, D)
                rocket.update_draw(ax_b)
            elif i > rocket.frame_ss[0] and i < rocket.frame_ss[1]:
                rocket.age += 1
                rocket.update_draw(ax_b)
            elif i == rocket.frame_ss[1]:
                index_removed = rocket.remove_draw(D)
                decrement_all_index_D(index_removed, R)

    if i % 100 == 0:
        print(prints)

    if i == P.FRAMES_STOP - 1:
        print("DONE")
        _logger.get_ram_usage_mb()

    return D


def close_event():
    plt.close()

# sec_vid = ((P.FRAMES_STOP - P.FRAMES_START) / P.FPS)
# min_vid = ((P.FRAMES_STOP - P.FRAMES_START) / P.FPS) / 60
# print("len of vid: " + str(sec_vid) + " s" + "    " + str(min_vid) + " min")

time0 = time.perf_counter()
# start_t = time.time()
ani = animation.FuncAnimation(fig, animate,
                              frames=range(P.FRAMES_START, P.FRAMES_STOP),
                              blit=True, interval=1, init_func=init,
                              repeat=False)  # interval only affects live ani. blitting seems to make it crash

if P.WRITE == 0:
    plt.show()
else:
    ani.save('./vids/vid_' + str(P.WRITE) + '_' + P.VID_SINGLE_WORD + '_' + '.mp4', writer=writer)

time1 = time.perf_counter() - time0
print("time1: " + str(time1))

# tot_time = round((time.time() - start_t) / 60, 4)
# print("minutes to make animation: " + str(tot_time) + " |  min_gen/min_vid: " + str(tot_time / min_vid))  #

min_vid = ((P.FRAMES_STOP - P.FRAMES_START) / P.FPS) / 60
sec_per_1_min = int(time1 / min_vid)
print("sec_per_1_min: " + str(sec_per_1_min))

_logger.row[9] = int(sec_per_1_min)

_logger.get_ram_usage_mb()
if P.SAVE == 1:
    _logger.add_save()


# if 'Rockets' in P.OBJ_TO_SHOW:
#     for rocket in R:
#         if i >= rocket.frame_ss[0] and rocket.drawn == 0:  # start_draw
#             rocket.set_age(i)
#         elif rocket.drawn == 1:
#             rocket.set_age(i)
#             rocket.start_draw(ax_b, D)
#         elif rocket.drawn == 2:
#             rocket.set_age(i)  # sets drawn
#             # index_removed = rocket.update_draw()
#             # index_removed = rocket.ani_update_step(ax_b, D)
#             if rocket.drawn == 2:
#                 _ = rocket.update_draw(ax_b)
#                 # set_data_rocket(rocket, ax_b)
#             elif rocket.drawn == 3:
#                 index_removed = rocket.ani_update_step(ax_b, D)
#                 prints += "  removing rocket"
#                 decrement_all_index_D(index_removed, R)
