from scipy.stats import beta
from src.m_functions import *

import P as P
from src.objects.o0 import O0C
from src.objects.o1 import O1C
from src.objects.rocket import Rocket



class GenObjects:

    """
    OBS this time it's only the background that is being ax.shown here. The other ax objects are added and
    deleted within the animation loop to save CPU-time.
    Each pic is tied to exactly 1 class instance and that class instance takes info from either o0 parent
    or other.
    """

    def __init__(_s):
        _s.pics = None
        _s.gis = None
        _s._years_days = None



    def gen_calidus(_s):
        """
        Base objects.
        """

        # for o0_id in P.O0_TO_SHOW:  # number_id
        o0_gi = _s.gis['Calidus']
        pic = _s.pics['0_red']  # HAVE TO to get centroid
        # O0[o0_id] = O0C(pic=None, gi=o0_gi)  # No pic CURRENTLY
        o0 = O0C(pic=pic, gi=o0_gi)  # NEEDS pic for centroid
        pi_offset_distr = [0, 0.3333 * 2 * np.pi, 0.6666 * 2 * np.pi]

        if P.REAL_SCALE == False:
            pic_black = _s.pics['0_black']
            gi = _s.gis['0_black']
            o1 = O1C(o1_id='0_black', gi=gi, pics_planet=[pic_black], parent=o0, type='0_static')  # THE PIC IS ALWAYS TIED TO 1 INSTANCE?
            o1.zorder = gi['zorder']
            o1.alpha = gi['alpha']
            o1.scale = gi['scale']
            o0.O1['0_black'] = o1

        pic_sun = _s.pics['0_sun']
        gi = _s.gis['0_sun']
        o1 = O1C(o1_id='0_sun', gi=gi, pics_planet=[pic_sun], parent=o0, type='0_static')  # THE PIC IS ALWAYS TIED TO 1 INSTANCE?
        o1.zorder = gi['zorder']
        o1.alpha = gi['alpha']
        if 'Calidus' not in P.OBJ_TO_SHOW and P.REAL_SCALE == False:
            o1.alpha = 0.1
        o1.scale = gi['scale']
        o0.O1['0_sun'] = o1

        if 'Calidus' in P.OBJ_TO_SHOW:

            pic_red = _s.pics['0_red']
            gi = _s.gis['0_red']
            o1 = O1C(o1_id='0_red', gi=gi, pics_planet=[pic_red], parent=o0, type='0_')  # THE PIC IS ALWAYS TIED TO 1 INSTANCE?
            o1.gen_calidus_astro(pi_offset_distr[0])
            o0.O1['0_red'] = o1
            #
            pic_mid = _s.pics['0_mid']
            gi = _s.gis['0_mid']
            o1 = O1C(o1_id='0_mid', gi=gi, pics_planet=[pic_mid], parent=o0, type='0_')
            o1.gen_calidus_astro(pi_offset_distr[1])
            o0.O1['0_mid'] = o1

            pic_light = _s.pics['0_light']
            gi = _s.gis['0_light']
            o1 = O1C(o1_id='0_light', gi=gi, pics_planet=[pic_light], parent=o0, type='0_')
            o1.gen_calidus_astro(pi_offset_distr[2])
            o0.O1['0_light'] = o1

            pic_0h_red = _s.pics['0h_red']
            gi = _s.gis['0h_red']
            o1 = O1C(o1_id='0h_red', gi=gi, pics_planet=[pic_0h_red], parent=o0, type='0_')
            o1.gen_calidus_astro(pi_offset_distr[0])
            o0.O1['0h_red'] = o1

            pic_0h_mid = _s.pics['0h_mid']
            gi = _s.gis['0h_mid']
            o1 = O1C(o1_id='0h_mid', gi=gi, pics_planet=[pic_0h_mid], parent=o0, type='0_')
            o1.gen_calidus_astro(pi_offset_distr[1])
            o0.O1['0h_mid'] = o1

            pic_0h_light = _s.pics['0h_light']
            gi = _s.gis['0h_light']
            o1 = O1C(o1_id='0h_light', gi=gi, pics_planet=[pic_0h_light], parent=o0, type='0_')
            o1.gen_calidus_astro(pi_offset_distr[2])
            o0.O1['0h_light'] = o1

        return o0

    def gen_planets_moons(_s, o0calidus):
        """
        """

        # time0 = time.time()

        if 'Ogun' in P.OBJ_TO_SHOW:
            gi = _s.gis['Ogun']
            pics_planet = _s.pics['Ogun']
            o1ogun = O1C(o1_id='Ogun', gi=gi, pics_planet=pics_planet, parent=o0calidus, type='body')  # THE PIC IS ALWAYS TIED TO 1 INSTANCE?
            o1ogun.gen_orbit()
            o1ogun.gen_DL()
            o0calidus.O1['Ogun'] = o1ogun

        if 'Venus' in P.OBJ_TO_SHOW:
            gi = _s.gis['Venus']
            pics_planet = _s.pics['Venus']
            o1ogun = O1C(o1_id='Venus', gi=gi, pics_planet=pics_planet, parent=o0calidus, type='body')  # THE PIC IS ALWAYS TIED TO 1 INSTANCE?
            o1ogun.gen_orbit()
            o1ogun.gen_DL()
            o0calidus.O1['Venus'] = o1ogun

        if 'Nauvis' in P.OBJ_TO_SHOW:
            gi = _s.gis['Nauvis']
            pics_planet = _s.pics['Nauvis']
            o1nauvis = O1C(o1_id='Nauvis', gi=gi, pics_planet=pics_planet, parent=o0calidus, type='body')  # THE PIC IS ALWAYS TIED TO 1 INSTANCE?
            o1nauvis.gen_orbit()
            o1nauvis.gen_DL()
            o1nauvis.children = ['GSS', 'Molli']
            o0calidus.O1['Nauvis'] = o1nauvis

            for child_id in o1nauvis.children:
                if child_id in P.OBJ_TO_SHOW:
                    gi = _s.gis[child_id]
                    pics_planet = _s.pics[child_id]
                    _o1 = O1C(o1_id=child_id, gi=gi, pics_planet=pics_planet, parent=o1nauvis, type='body')  # THE PIC IS ALWAYS TIED TO 1 INSTANCE?
                    _o1.gen_orbit()
                    _o1.gen_DL()
                    o0calidus.O1[child_id] = _o1

        if 'Mars' in P.OBJ_TO_SHOW:
            gi = _s.gis['Mars']
            pics_planet = _s.pics['Mars']
            o1mars = O1C(o1_id='Mars', gi=gi, pics_planet=pics_planet, parent=o0calidus, type='body')  # THE PIC IS ALWAYS TIED TO 1 INSTANCE?
            o1mars.gen_orbit()
            o1mars.gen_DL()
            o0calidus.O1['Mars'] = o1mars

        if 'Jupiter' in P.OBJ_TO_SHOW:
            gi = _s.gis['Jupiter']
            pics_planet = _s.pics['Jupiter']
            o1jupiter = O1C(o1_id='Jupiter', gi=gi, pics_planet=pics_planet, parent=o0calidus, type='body')  # THE PIC IS ALWAYS TIED TO 1 INSTANCE?
            o1jupiter.gen_orbit()
            o1jupiter.gen_DL()
            o1jupiter.children = ['Everglade', 'Petussia']
            o0calidus.O1['Jupiter'] = o1jupiter

            for child_id in o1jupiter.children:
                if child_id in P.OBJ_TO_SHOW:
                    # o1gss = None
                    gi = _s.gis[child_id]
                    pics_planet = _s.pics[child_id]
                    o1gss = O1C(o1_id=child_id, gi=gi, pics_planet=pics_planet, parent=o1jupiter, type='body')  # THE PIC IS ALWAYS TIED TO 1 INSTANCE?
                    o1gss.gen_orbit()
                    o1gss.gen_DL()
                    o0calidus.O1[child_id] = o1gss

        if 'Astro0' in P.OBJ_TO_SHOW:
            gi = _s.gis['Astro0']
            pic_planet = _s.pics['Astro0']
            o1astro0 = O1C(o1_id='Astro0', gi=gi, pics_planet=[pic_planet], parent=o0calidus, type='astro')  # THE PIC IS ALWAYS TIED TO 1 INSTANCE?
            o1astro0.gen_astro0()
            o0calidus.O1['Astro0'] = o1astro0

        if 'Astro0b' in P.OBJ_TO_SHOW:
            gi = _s.gis['Astro0b']
            pics_planet = _s.pics['Astro0b']
            _o1 = O1C(o1_id='Astro0b', gi=gi, pics_planet=pics_planet, parent=o0calidus, type='body')  # THE PIC IS ALWAYS TIED TO 1 INSTANCE?
            _o1.gen_orbit()
            _o1.gen_DL()
            o0calidus.O1['Astro0b'] = _o1

        if 'Saturn' in P.OBJ_TO_SHOW:
            gi = _s.gis['Saturn']
            pics_planet = _s.pics['Saturn']
            o1saturn = O1C(o1_id='Saturn', gi=gi, pics_planet=pics_planet, parent=o0calidus, type='body')  # THE PIC IS ALWAYS TIED TO 1 INSTANCE?
            o1saturn.gen_orbit()
            o1saturn.gen_DL()
            o0calidus.O1['Saturn'] = o1saturn

        if 'Uranus' in P.OBJ_TO_SHOW:
            gi = _s.gis['Uranus']
            pics_planet = _s.pics['Uranus']
            o1uranus = O1C(o1_id='Uranus', gi=gi, pics_planet=pics_planet, parent=o0calidus, type='body')  # THE PIC IS ALWAYS TIED TO 1 INSTANCE?
            o1uranus.gen_orbit()
            o1uranus.gen_DL()
            o0calidus.O1['Uranus'] = o1uranus

        if 'Neptune' in P.OBJ_TO_SHOW:
            gi = _s.gis['Neptune']
            pics_planet = _s.pics['Neptune']
            o1neptune = O1C(o1_id='Neptune', gi=gi, pics_planet=pics_planet, parent=o0calidus, type='body')  # THE PIC IS ALWAYS TIED TO 1 INSTANCE?
            o1neptune.gen_orbit()
            o1neptune.gen_DL()
            o0calidus.O1['Neptune'] = o1neptune

        return o0calidus

    def gen_rockets(_s, o0calidus):

        R = []

        R_gi = _s.gis['Rockets']

        for i in range(len(R_gi)):  # OBS ITERABLE LIST
            # for i in range(1):
            roc_gi = R_gi[i]

            if roc_gi['od'][0] not in P.OBJ_TO_SHOW or roc_gi['od'][1] not in P.OBJ_TO_SHOW:
                continue
            p0 = o0calidus.O1[roc_gi['od'][0]]
            p1 = o0calidus.O1[roc_gi['od'][1]]

            _destination_type = 'inter'
            if (p0.id == 'Nauvis' and p1.id == 'GSS'):
                _destination_type = 'orbit'

            # init_frames = _s.gen_init_frames(p0, p1, roc_gi, _destination_type)
            init_frames = [5, 25, 50, 100, 200, 500, 700]

            for init_frame in init_frames:

                rocket = Rocket(init_frame=init_frame, gi=roc_gi, p0=p0, p1=p1, destination_type=_destination_type)
                rocket.gen_rocket_motion()
                # TODO: check frame overflow here
                # if ok_rocket == '':
                R.append(rocket)

            # R.append(rocket2)

        return R

    def gen_rockets_seq(_s, o0calidus):

        R = []
        # R_gi = _s.gis['Rockets_seq']

        R_gi = [{'od': ['GSS', 'Astro0b'], 'frames_delay': 0},
                {'od': ['Astro0b', 'Everglade'], 'frames_delay': 100},
                {'od': ['Everglade', 'GSS'], 'frames_delay': 50}
                ]

        init_frame = 200

        for i in range(len(R_gi)):  # OBS ITERABLE LIST
            roc_gi = R_gi[i]

            p0 = o0calidus.O1[roc_gi['od'][0]]
            p1 = o0calidus.O1[roc_gi['od'][1]]

            _destination_type = 'inter'
            if (p0.id == 'Nauvis' and p1.id == 'GSS'):
                _destination_type = 'orbit'

            rocket = Rocket(init_frame=init_frame, gi=roc_gi, p0=p0, p1=p1, destination_type=_destination_type)
            rocket.gen_rocket_motion()

            init_frame = rocket.frame_ss[1] + roc_gi['frames_delay']

            R.append(rocket)

        R_gi2 = [
            {'od': ['Ogun', 'Astro0b']},
            {'od': ['Molli', 'Astro0b']},
            {'od': ['Everglade', 'Astro0b']}
        ]

        for i in range(len(R_gi2)):  # OBS ITERABLE LIST

            roc_gi = R_gi2[i]

            p0 = o0calidus.O1[roc_gi['od'][0]]
            p1 = o0calidus.O1[roc_gi['od'][1]]

            _destination_type = 'inter'
            if (p0.id == 'Nauvis' and p1.id == 'GSS'):
                _destination_type = 'orbit'

            rocket = Rocket(init_frame=init_frame, gi=roc_gi, p0=p0, p1=p1, destination_type=_destination_type)
            rocket.gen_rocket_motion()

            R.append(rocket)

        return R

    def gen_init_frames(_s, p0, p1, roc_gi, destination_type):
        """
        For rockets based on distances (dp0p1) and distance gradients between two planets.
        The sampling is beta-discrete from an argsort.

        init_frames_cands ALLOWS all frames in planet motions. Cleaned up AFTER selection
        The ddist are argsorted, then samples are taken from this argsort.
        """

        num_to_select = P.FRAMES_TOT // roc_gi['init_frame_step']

        dist = -np.asarray([np.linalg.norm(p0.xy[i, :] - p1.xy[i, :]) for i in range(len(p0.xy))])
        dist_grad = np.gradient(dist, axis=0)  # MUST BE BASED ON unsorted

        dist = min_max_normalize_array(dist, y_range=[0, 1])
        dist_grad = min_max_normalize_array(dist_grad, y_range=[0, 1])  # seems to work for neg vals

        ddd = 0.3 * dist + 0.7 * dist_grad
        ddd = min_max_normalize_array(ddd, y_range=[0, 1])

        ddd_inds_sorted = np.argsort(ddd)[::-1]  #

        '''OBS this pdf gives the probability that a frame will be sampled based on ddd
        loc=30 means that the 30 frames when p0 and p1 are too close won't be sampled '''
        pdf_dist = beta.pdf(x=np.arange(0, len(p0.xy)), loc=30, a=2, b=6, scale= len(p0.xy))  # 2 6
        if destination_type == 'orbit':
            pdf_dist = beta.pdf(x=np.arange(0, len(p0.xy)), loc=30, a=2, b=2, scale=1 * len(p0.xy))  # 2 6
        pdf_dist /= np.sum(pdf_dist)  # only works for pos?
        # dist_inds_sorted_subset = np.random.choice(dist_inds_sorted, size=len(p0.xy) // 2, replace=False, p=pdf_dist)
        # dist_inds_sorted_subset = np.random.choice(dist_inds_sorted, size=num_to_select * 2, replace=False, p=pdf_dist)
        init_frames = np.sort(np.random.choice(ddd_inds_sorted, size=num_to_select, replace=False, p=pdf_dist))
        init_frames = init_frames[np.where(init_frames > 5)]
        # init_frames = init_frames[np.where(init_frames + 2000 + roc_gi['frames_max'] < P.FRAMES_TOT_BODIES)]
        init_frames = init_frames[np.where(init_frames + 2000 < P.FRAMES_TOT_BODIES)]

        # min_distance_integers =
        # filtered = [arr[0]]  # Always keep the first element
        # for num in arr[1:]:
        #     if num - filtered[-1] >= 100:
        #         filtered.append(num)

        init_frames = list(init_frames)
        return init_frames




# ddist_subset = ddist[dist_inds_sorted_subset]
# ddist_subset_inds_sorted = np.argsort(ddist_subset)
# pdf_ddist = beta.pdf(x=np.arange(0, len(dist_inds_sorted_subset)), a=2, b=6, loc=0,
#                      scale=len(dist_inds_sorted_subset))
# pdf_ddist /= np.sum(pdf_ddist)
# init_frames = np.sort(np.random.choice(ddist_subset_inds_sorted, size=num_to_select, replace=False, p=pdf_ddist))


# aa = np.random.choice(np.array([1, 2, 3, 4, 5]), size=5, replace=False, p=[0.05, 0.05, 0.1, 0.4, 0.4])
# init_frames = np.arange(start=5, stop=P.FRAMES_TOT_BODIES - 200, step=roc_gi['init_frame_step'])
# init_frames += np.random.randint(low=-roc_gi['init_frame_step'] // 2,
#                                  high=roc_gi['init_frame_step'] // 2,
#                                  size=len(init_frames))
# init_frames = np.array([init_frames[6]])