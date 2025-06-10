

import P
from src.objects.abstract_all import AbstractObject
from src.a_pygame.draw_helpers_pygame import *

class AbstractPygameObject(AbstractObject):
    
    def __init__(_s):
        AbstractObject.__init__(_s)

        _s.surf = None
        _s.rect = None

        # ONLY USED BY o1 'body' type:
        _s.surfs_DL = []
        _s.rects_DL = []

    def start_draw(_s, D):
        """
        Called when object becomes visible (drawn == 1).
        """

        if _s.type == 'body':

            for k in range(len(_s.pics_planet)):
                pic = _s.pics_planet[k]
                surf = to_surface(pic)  # Assume self.pic is a NumPy array
                rect = surf.get_rect()

                _s.surfs_DL.append(surf)
                _s.rects_DL.append(rect)

                D.append((_s.zorders_DL[k][0], _s.type, (surf, rect.topleft)))

        elif _s.type == '0_static':

            _s.surf = to_surface(_s.pic)

            r = int(_s.surf.get_height() / 2 * _s.scale)
            size = 2 * r

            _s.surf = pygame.transform.smoothscale(_s.surf, (size, size))
            _s.surf.set_alpha(int(_s.alpha * 255))

            _s.rect = _s.surf.get_rect()

            _s.rect.topleft = (P.MAP_DIMS[0] / 2 - r, P.MAP_DIMS[1] / 2 - r)
            D.append((_s.zorder, _s.type, (_s.surf, _s.rect.topleft)))

        elif _s.type in ['0_', 'astro']:
            _s.surf = to_surface(_s.pic)
            _s.rect = _s.surf.get_rect()

            D.append((_s.zorders[0], _s.type, (_s.surf, _s.rect.topleft)))

        elif _s.type == 'rocket':
            pass

        # else:
        #     if not hasattr(_s, 'surf'):
        #         _s.surf = to_surface(_s.pic)  # Assume self.pic is a NumPy array
        #         _s.rect = _s.surf.get_rect()
        #     else:
        #         raise Exception("Asdfasdf")

            # raise Exception("Double check")

    def update_draw(_s, D):

        if _s.type == 'body':
            xy = _s.xy[_s.age]
            rot = _s.rotation[_s.age]
            scale = _s.scale[_s.age]

            for k in range(len(_s.pics_planet)):

                surf = _s.surfs_DL[k]

                # SCALING ====
                w, h = surf.get_size()
                surf = pygame.transform.smoothscale(surf, (int(w * scale), int(h * scale)))

                # ROTATION ====
                surf = pygame.transform.rotate(surf, -np.degrees(rot))

                # ALPHA ====
                # alpha_f =
                surf.set_alpha(int(_s.alphas_DL[k][_s.age] * 255))

                z = _s.zorders_DL[k][_s.age]
                rect = surf.get_rect(center=(round(xy[0]), round(xy[1])))
                # rect = _s.rects_DL[k]  # DOESNT WORK
                D.append((z, _s.type, (surf, rect.topleft)))

        elif _s.type == '0_static':
            D.append((_s.zorder, _s.type, (_s.surf, _s.rect.topleft)))
        elif _s.type in ['0_']:

            xy = _s.xy[_s.age]
            rot = _s.rotation[_s.age]
            scale = _s.scale[_s.age]
            surf = _s.surf

            # SCALING ====
            w, h = surf.get_size()
            surf = pygame.transform.smoothscale(surf, (int(w * scale), int(h * scale)))

            # ROTATION ====
            surf = pygame.transform.rotate(surf, -np.degrees(rot))
            # rect = surf.get_rect(center=(int(xy[0]), int(xy[1])))
            rect = surf.get_rect(center=(round(xy[0]), round(xy[1])))

            # ALPHA ====
            # alpha_f = _s.alphas[_s.age]
            surf.set_alpha(int(_s.alphas[_s.age] * 255))

            z = _s.zorders[_s.age]
            D.append((z, _s.type, (surf, rect.topleft)))

        elif _s.type == 'astro':

            surf = _s.surf
            alpha = int(_s.alphas[_s.age] * 255)
            z = int(_s.zorders[_s.age])
            rot_dynamic = -np.degrees(_s.rotation[_s.age])  # negate for Pygame rotation
            rot_fixed = -np.degrees(0.3)  # static tilt ≈ -17.2°

            # Step 1: First rotation (dynamic)
            surf = pygame.transform.rotate(surf, rot_dynamic)

            # Step 2: Scale
            w, h = surf.get_size()
            surf = pygame.transform.smoothscale(surf, (int(w * 1.3), int(h * 0.25)))

            # Step 3: Second rotation (static tilt)
            surf = pygame.transform.rotate(surf, rot_fixed)

            # Step 4: Set alpha
            surf.set_alpha(alpha)

            # Step 5: Positioning
            rect = surf.get_rect(center=(P.MAP_DIMS[0] / 2, P.MAP_DIMS[1] / 2))  # rotate_around anchor

            D.append((z, _s.type, (surf, rect.topleft)))

        elif _s.type == 'rocket':

            x, y = _s.xy[_s.age]
            z = _s.zorders[_s.age]
            alpha = int(_s.alphas[_s.age] * 255)

            # Convert color from float to 0–255
            # color = tuple(int(c * 255) for c in _s.color[_s.age])
            color = int(_s.color[_s.age] * 255)

            # Radius: 1 or 2 depending on resolution
            radius = 1

            # Store drawing command into D
            D.append((z, _s.type, (color, (int(x), int(y)), radius, alpha)))







