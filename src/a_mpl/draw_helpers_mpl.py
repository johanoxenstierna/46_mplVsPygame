
# import cv2
import numpy as np
import random
from copy import deepcopy
import P
from scipy.stats import multivariate_normal
from src.m_functions import min_max_normalization
import matplotlib.transforms as mtransforms
import matplotlib.pyplot as plt

def gen_backgr(pics, ax_b):
	""""""
	ax_b.imshow(pics['backgr_b'], zorder=1, alpha=0.99)
	ax_b.imshow(pics['backgr_55'], zorder=2, alpha=0.1)

	if P.WRITE != 0:
		ax_b.axis([0, P.MAP_DIMS[0], 0, P.MAP_DIMS[1]])
	else:
		# ax_b.axis([850, 1250, 500, 700])   # nice for runnning faster/debugging
		# ax_b.axis([450, 1450, 300, 800])
		ax_b.axis([0, P.MAP_DIMS[0], 0, P.MAP_DIMS[1]])

	ax_b.axis('off')  # TURN ON FOR FINAL
	ax_b.set_axis_off()

def decrement_all_index_D(index_removed, R):
	"""
	Whenever an D is popped from the list, all index_D with higher index will be wrong and
	need to be decremented by 1.
	"""

	for rocket in R:
		if rocket.index_D != None:  # if the object was not the one removed
			if rocket.index_D > index_removed:
				rocket.index_D -= 1


# def update_draw(o, ax_b):
# 	"""
# 	OBS the planets are NEVER REMOVED
# 	"""
#
# 	if o.type == 'body':
# 		if len(o.pics_planet) > 1:
# 			for i in range(len(o.D_o1)):  # DL
# 				ax0 = o.D_o1[i]
# 				M = mtransforms.Affine2D(). \
# 						scale(o.scale[o.age]). \
# 						rotate_around(o.centroids[o.age], o.centroids[o.age], o.rotation[o.age]). \
# 						translate(o.xy[o.age][0], o.xy[o.age][1]). \
# 						translate(-o.centroids[o.age], -o.centroids[o.age]) + ax_b.transData
#
# 				ax0.set_transform(M)
# 				ax0.set_alpha(o.alphas_DL[i][o.age])
# 				ax0.set_zorder(int(o.zorders_DL[i][o.age]))
#
# 		else:  # NO for loop!
# 			ax0 = o.D_o1[0]
# 			M = mtransforms.Affine2D(). \
# 				scale(o.scale[o.age]). \
# 				rotate_around(o.centroids[o.age], o.centroids[o.age], o.rotation[o.age]). \
# 				translate(o.xy[o.age][0], o.xy[o.age][1]). \
# 				translate(-o.centroids[o.age], -o.centroids[o.age]) + ax_b.transData
# 			ax0.set_transform(M)
# 			ax0.set_alpha(o.alphas[o.age])
# 			ax0.set_zorder(int(o.zorders[o.age]))
#
# 		if o.id == 'Nauvis' and 'YearsDays' in P.OBJ_TO_SHOW:
# 			o.ax_year_day.set_text(o.years_days[o.age])
# 	elif o.type in ['0_']:
# 		M = mtransforms.Affine2D(). \
# 			scale(o.scale[o.age]). \
# 			rotate_around(o.centroids[o.age], o.centroids[o.age], o.rotation[o.age]). \
# 			translate(o.xy[o.age][0], o.xy[o.age][1]). \
# 			translate(-o.centroids[o.age], -o.centroids[o.age]) + ax_b.transData
# 		o.ax0.set_transform(M)
# 		o.ax0.set_alpha(o.alphas[o.age])
# 		o.ax0.set_zorder(int(o.zorders[o.age]))
# 	elif o.type in['0_static']:  # KEEP THIS: PLACEHOLDER FOR 'SUN'
# 		pass
# 	elif o.type in ['astro']:
# 		# M = mtransforms.Affine2D(). \
# 		# 		rotate_around(530, 540, o.rotation[o.age]). \
# 		# 		scale(1.3, 0.2). \
# 		# 		skew(0, 0.3). \
# 		# 		translate(260, 215) + ax_b.transData
#
# 		M = mtransforms.Affine2D(). \
# 				rotate_around(530, 540, o.rotation[o.age]). \
# 				scale(1.3, 0.25). \
# 				rotate_around(530, 540, 0.3). \
# 				translate(150, 350) + ax_b.transData
#
# 		if P.REAL_SCALE == 1:
# 			M = mtransforms.Affine2D(). \
# 					rotate_around(540, 540, o.rotation[o.age]). \
# 					scale(0.7, 0.1). \
# 					skew(0, 0.3). \
# 					translate(580, 375) + ax_b.transData
#
# 		o.ax0.set_transform(M)
# 		o.ax0.set_alpha(o.alphas[o.age])
# 		o.ax0.set_zorder(int(o.zorders[o.age]))
# 	else:
# 		raise Exception("This o1 does not exist*&&*(")


def set_data_rocket(o, D):
	"""
	OBS centroid shifting is done in rocket.py
	"""
	xys_cur = [[o.xy[o.age, 0]], [o.xy[o.age, 1]]]
	# D[o.index_D].set_data(xys_cur)  # SELECTS A SUBSET OF WHATS ALREADY PLOTTED
	o.ax0.set_data(xys_cur)  # SELECTS A SUBSET OF WHATS ALREADY PLOTTED
	o.ax0.set_alpha(o.alphas[o.age])
	o.ax0.set_zorder(o.zorders[o.age])
	# o.ax0.set_linewidth(100)  # not doing anything
	o.ax0.set_color((o.color[o.age], o.color[o.age], o.color[o.age]))

	# plt.setp(D[o.index_D], markersize=10)





