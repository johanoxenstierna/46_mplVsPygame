import pygame
import numpy as np


def to_surface(arr):

    if arr.dtype != np.uint8:  # Pygame must reformat the dtype to uint8
        arr = np.clip(arr * 255, 0, 255).astype(np.uint8)

    if arr.ndim == 2:
        # arr = np.stack([arr]*3, axis=-1)
        raise Exception("ndim==2")

    arr = np.transpose(arr, (1, 0, 2))  # (H, W, C) → (W, H, C)

    rgb = arr[:, :, :3]
    alpha = arr[:, :, 3]

    surf = pygame.Surface(arr.shape[:2], pygame.SRCALPHA).convert_alpha()
    pygame.surfarray.blit_array(surf, rgb)
    pygame.surfarray.pixels_alpha(surf)[:, :] = alpha
    return surf


def gen_backgr(pics):
    """Returns a background surface created from two overlaid images."""
    base_arr = pics['backgr_b']
    overlay_arr = pics['backgr_55']
    # test = pics['Nauvis'][0]
    # overlay_test = to_surface(test, keep_alpha=True)
    base_surf = to_surface(base_arr)
    overlay_surf = to_surface(overlay_arr)
    overlay_surf.set_alpha(int(0.1 * 255))

    base_surf.blit(overlay_surf, (0, 0))

    return base_surf
