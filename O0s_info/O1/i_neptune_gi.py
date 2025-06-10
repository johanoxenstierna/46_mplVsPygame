



import numpy as np
import P

def neptune_gi_():  # 20

    gi = {}
    gi['r'] = 1300
    gi['pi_offset'] = 0.9 * 2 * np.pi
    gi['speed_gi'] = 0.2  # 4
    gi['tilt'] = 0.07 * 2 * np.pi
    gi['scale'] = 0.4
    gi['centroid_mult'] = 4

    if P.REAL_SCALE == 1:
        gi['r'] = 4500
        gi['pi_offset'] = 0.01 * 2 * np.pi
        gi['scale'] = 0.01
        gi['speed_gi'] = 0.07

    return gi