
import matplotlib.transforms as mtransforms

import P
from src.objects.abstract_all import AbstractObject

class AbstractMPLObject(AbstractObject):

    def __init__(_s):
        AbstractObject.__init__(_s)
        _s.index_D = None  # OBS USED BY ROCKET
        _s.D_inds = []  # OBS ASSUMES OBJS NEVER REMOVED
        _s.D_o1 = []

    def ani_update_step(_s, ax_b, D):
        """
        Based on the drawn condition, draw, remove
        If it's drawn, return True (used in animation loop)
        OBS major bug discovered: D.pop(index_axs0) OBVIOUSLY results in that all index_axs0 after popped get
        screwed.
        Returns the following index:
        0: don't draw
        1: draw (will result in warp_affine)
        2: ax has just been removed, so decrement all index_axs0
        """

        D[_s.index_D].remove()  # might save CPU-time
        D.pop(_s.index_D)  # OBS OBS!!! MAKES axs0 shorter hence all items after index_axs0 now WRONG
        index_removed = _s.index_D
        _s.index_D = None  # THIS IS NEEDED BUT NOT SURE WHY

        return index_removed

    def start_draw(_s, ax_b, D):

        '''This is where picture copy is created'''
        if _s.type in ['body', '0_', '0_static', 'astro']:
            if _s.type == 'body':
                for pic in _s.pics_planet:
                    D.append(ax_b.imshow(pic, zorder=_s.zorder, alpha=0, interpolation='nearest'))
                    _s.D_inds.append(len(D) - 1)  # THIS -1 IS NEW: Earlier it was done above
                    _s.D_o1.append(D[-1])

                if _s.id == 'Nauvis' and 'YearsDays' in P.OBJ_TO_SHOW:
                    year_day = ax_b.text(
                        0.05, 0.1,  # Relative coords (x, y) in axis fraction (0 to 1)
                        'sfgsdfgfd',  # Initial blank text
                        transform=ax_b.transAxes,  # Make sure coords are relative to axes
                        fontsize=12,
                        color='white',
                        # ha='left', va='bottom',
                        zorder=10000  # Ensure it's above everything else
                    )
                    _s.ax_year_day = year_day
                    D.append(year_day)  # Optional: keep consistent with your system
            elif _s.type in ['0_', 'astro']:
                D.append(ax_b.imshow(_s.pic, zorder=_s.zorder, alpha=0))
                _s.ax0 = D[len(D) - 1]
            elif _s.type == '0_static':

                r = int(_s.pic.shape[0] / 2 * _s.scale)
                extent = [P.MAP_DIMS[0] / 2 - r, P.MAP_DIMS[0] / 2 + r,
                          P.MAP_DIMS[1] / 2 + r, P.MAP_DIMS[1] / 2 - r]

                D.append(ax_b.imshow(_s.pic, zorder=_s.zorder, alpha=_s.alpha, extent=extent))
                # D.append(ax_b.imshow(_s.pic, extent=extent))

                # ax_b.imshow(_s.pic, zorder=3000, alpha=0.9, extent=extent)
                _s.ax0 = D[len(D) - 1]

        elif _s.type == 'rocket':
            _s.index_D = len(D)
            D.append(ax_b.plot(_s.xy[0, 0], _s.xy[0, 1], zorder=_s.zorder,
                               alpha=0, color=(0.99, 0.99, 0.99), marker='o', markersize=1)[0])
            _s.ax0 = D[_s.index_D]

        else:
            raise Exception("notthing added in ani_update_step")

        return None

    def update_draw(_s, ax_b):
        if _s.type == 'body':
            if len(_s.pics_planet) > 1:
                for i in range(len(_s.D_o1)):  # DL
                    ax0 = _s.D_o1[i]
                    M = mtransforms.Affine2D(). \
                            scale(_s.scale[_s.age]). \
                            rotate_around(_s.centroids[_s.age], _s.centroids[_s.age], _s.rotation[_s.age]). \
                            translate(_s.xy[_s.age][0], _s.xy[_s.age][1]). \
                            translate(-_s.centroids[_s.age], -_s.centroids[_s.age]) + ax_b.transData

                    ax0.set_transform(M)
                    ax0.set_alpha(_s.alphas_DL[i][_s.age])
                    ax0.set_zorder(int(_s.zorders_DL[i][_s.age]))

            else:  # NO for loop!
                ax0 = _s.D_o1[0]
                M = mtransforms.Affine2D(). \
                        scale(_s.scale[_s.age]). \
                        rotate_around(_s.centroids[_s.age], _s.centroids[_s.age], _s.rotation[_s.age]). \
                        translate(_s.xy[_s.age][0], _s.xy[_s.age][1]). \
                        translate(-_s.centroids[_s.age], -_s.centroids[_s.age]) + ax_b.transData
                ax0.set_transform(M)
                ax0.set_alpha(_s.alphas[_s.age])
                ax0.set_zorder(int(_s.zorders[_s.age]))

            if _s.id == 'Nauvis' and 'YearsDays' in P.OBJ_TO_SHOW:
                _s.ax_year_day.set_text(_s.years_days[_s.age])
        elif _s.type in ['0_']:
            M = mtransforms.Affine2D(). \
                    scale(_s.scale[_s.age]). \
                    rotate_around(_s.centroids[_s.age], _s.centroids[_s.age], _s.rotation[_s.age]). \
                    translate(_s.xy[_s.age][0], _s.xy[_s.age][1]). \
                    translate(-_s.centroids[_s.age], -_s.centroids[_s.age]) + ax_b.transData
            _s.ax0.set_transform(M)
            _s.ax0.set_alpha(_s.alphas[_s.age])
            _s.ax0.set_zorder(int(_s.zorders[_s.age]))
        elif _s.type in ['0_static']:  # KEEP THIS: PLACEHOLDER FOR 'SUN'
            pass
        elif _s.type in ['astro']:
            # M = mtransforms.Affine2D(). \
            # 		rotate_around(530, 540, _s.rotation[_s.age]). \
            # 		scale(1.3, 0.2). \
            # 		skew(0, 0.3). \
            # 		translate(260, 215) + ax_b.transData

            M = mtransforms.Affine2D(). \
                    rotate_around(530, 540, _s.rotation[_s.age]). \
                    scale(1.3, 0.25). \
                    rotate_around(530, 540, 0.3). \
                    translate(150, 350) + ax_b.transData

            if P.REAL_SCALE == 1:
                M = mtransforms.Affine2D(). \
                        rotate_around(540, 540, _s.rotation[_s.age]). \
                        scale(0.7, 0.1). \
                        skew(0, 0.3). \
                        translate(580, 375) + ax_b.transData

            _s.ax0.set_transform(M)
            _s.ax0.set_alpha(_s.alphas[_s.age])
            _s.ax0.set_zorder(int(_s.zorders[_s.age]))

        elif _s.type == 'rocket':
            xys_cur = [[_s.xy[_s.age, 0]], [_s.xy[_s.age, 1]]]
            # D[_s.index_D].set_data(xys_cur)  # SELECTS A SUBSET OF WHATS ALREADY PLOTTED
            _s.ax0.set_data(xys_cur)  # SELECTS A SUBSET OF WHATS ALREADY PLOTTED
            _s.ax0.set_alpha(_s.alphas[_s.age])
            _s.ax0.set_zorder(_s.zorders[_s.age])
            # _s.ax0.set_linewidth(100)  # not doing anything
            _s.ax0.set_color((_s.color[_s.age], _s.color[_s.age], _s.color[_s.age]))

        else:
            raise Exception("This o1 does not exist*&&*(")

    def remove_draw(_s, D):
        D[_s.index_D].remove()  # might save CPU-time
        D.pop(_s.index_D)  # OBS OBS!!! MAKES axs0 shorter hence all items after index_axs0 now WRONG
        index_removed = _s.index_D
        _s.index_D = None  # THIS IS NEEDED BUT NOT SURE WHY

        return index_removed