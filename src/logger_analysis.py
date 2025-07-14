import numpy as np
import matplotlib.pyplot as plt
from typing import Literal

from logger_keys import logger_keys


def col_name(col_index):
    key = logger_keys.get(col_index)
    if isinstance(key, tuple):
        return key[0]
    return key


def value_label(col_index, val):
    key = logger_keys.get(col_index)
    if isinstance(key, tuple):
        return key[1].get(val, str(val))
    return str(val)


def subset_logger(logger, split_col, split_mode: Literal['both', 'only_low', 'only_high']):
    unique_vals = np.unique(logger[:, split_col])
    val_low, val_high = sorted(unique_vals)

    if split_mode == 'both':
        return {
            val_low: logger[logger[:, split_col] == val_low],
            val_high: logger[logger[:, split_col] == val_high]
        }
    elif split_mode == 'only_low':
        return logger[logger[:, split_col] == val_low]
    elif split_mode == 'only_high':
        return logger[logger[:, split_col] == val_high]
    else:
        raise ValueError(f"Invalid split_mode '{split_mode}'.")


def gen_3D_scatter(logger, split_col, x_col, y_col, z_col, split_mode='both'):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    color_map = {
        0: 'red',
        1: 'blue'
    }

    subset_data = subset_logger(logger, split_col, split_mode)

    if isinstance(subset_data, dict):
        for val, subset in subset_data.items():
            ax.scatter(subset[:, x_col], subset[:, y_col], subset[:, z_col],
                       c=color_map[val], label=f"{split_col=}: {int(val)}")
    else:
        val = np.unique(subset_data[:, split_col])[0]
        ax.scatter(subset_data[:, x_col], subset_data[:, y_col], subset_data[:, z_col],
                   c=color_map[val], label=f"{split_col=}: {int(val)}")

    ax.set_xlabel(f"Column {x_col}")
    ax.set_ylabel(f"Column {y_col}")
    ax.set_zlabel(f"Column {z_col}")
    ax.set_title(f"3D Scatter Split by Column {split_col} ({split_mode})")
    ax.legend()
    plt.tight_layout()
    plt.show()


def gen_2D_scatter_old(logger, split_col, x_col, y_col, split_mode='both', lin_reg_line=False):

    fig, ax = plt.subplots()

    color_map = {0: 'red', 1: 'blue'}

    subset_data = subset_logger(logger, split_col, split_mode)

    def plot_scatter(subset, color, label):
        x_vals = subset[:, x_col].astype(float)
        y_vals = subset[:, y_col].astype(float)
        ax.scatter(x_vals, y_vals, c=color, label=label)

        if lin_reg_line and len(x_vals) > 1:
            m, b = np.polyfit(x_vals, y_vals, deg=1)
            ax.plot(x_vals, m * x_vals + b, linestyle='--', color=color, label=f"{label} lin-reg")

    if isinstance(subset_data, dict):
        for val, subset in subset_data.items():
            label = f"{col_name(split_col)} = {value_label(split_col, val)}"
            plot_scatter(subset, color_map[val], label)
    else:
        val = int(np.unique(subset_data[:, split_col])[0])
        label = f"{col_name(split_col)} = {value_label(split_col, val)}"
        plot_scatter(subset_data, color_map[val], label)

    # ax.set_xlabel(f"Column {x_col}")
    # ax.set_ylabel(f"Column {y_col}")
    # ax.set_title(f"2D Scatter by Column {split_col} ({split_mode})")

    ax.set_xlabel(col_name(x_col))
    ax.set_ylabel(col_name(y_col))

    ax.legend()
    plt.tight_layout()
    plt.show()


def gen_2D_scatter(logger, split_col, x_col, y_col, split_mode='both', lin_reg_line=False, title=''):
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots()

    # Expecting only two unique values
    unique_vals = sorted(np.unique(logger[:, split_col]))
    if len(unique_vals) != 2:
        raise ValueError(f"Expected 2 unique values in split_col {split_col}, found {len(unique_vals)}: {unique_vals}")

    color_map = {
        unique_vals[0]: 'red',
        unique_vals[1]: 'blue'
    }

    subset_data = subset_logger(logger, split_col, split_mode)

    def plot_scatter(subset, color, label):
        x_vals = subset[:, x_col].astype(float)
        y_vals = subset[:, y_col].astype(float)
        ax.scatter(x_vals, y_vals, c=color, label=label)

        if lin_reg_line and len(x_vals) > 1:
            m, b = np.polyfit(x_vals, y_vals, deg=1)
            ax.plot(x_vals, m * x_vals + b, linestyle='--', color=color, label=f"{label} lin-reg")

    if isinstance(subset_data, dict):
        for val, subset in subset_data.items():
            label = f"{col_name(split_col)} = {value_label(split_col, val)}"
            plot_scatter(subset, color_map[val], label)
    else:
        val = int(np.unique(subset_data[:, split_col])[0])
        label = f"{col_name(split_col)} = {value_label(split_col, val)}"
        plot_scatter(subset_data, color_map[val], label)

    ax.set_xlabel(col_name(x_col))
    ax.set_ylabel(col_name(y_col))
    ax.set_title(title)
    ax.legend()
    plt.tight_layout()


def combine_features(logger, col6=6, col7=7, name='combined_feature'):
    """
    sqrt(avg_diam) * num_pngs
    col 6: num_pngs
    col 7: avg_diam
    col 13: combined
    """
    combined = logger[:, col6].astype(float) * np.sqrt(logger[:, col7].astype(float))
    combined = combined.reshape(-1, 1)
    combined = combined.astype(int)
    logger_with_combined = np.hstack([logger, combined])
    return logger_with_combined

# Ready for new logger file to test updated combine_features behavior

if __name__ == '__main__':
    logger = np.load('./src/logger.npy')
    logger = logger[1:, :]  # Skip header
    rows_write = np.where(logger[:, 5] != 0)[0]  # WRITE SET TO 1 ALWAYS
    logger[rows_write, 5] = 1
    logger = combine_features(logger)  # col 13: combined 6-7
    rows_mpl = np.where(logger[:, 1] == 0)[0]
    rows_pygame = np.where(logger[:, 1] == 1)[0]
    rows_only_largest = np.where(logger[:, 13] == 132)[0]

    # RESULTS =================
    # 1. Pygame Vs Matplotlib: Pygame 10x faster. It actually starts more like 15x and then decreases to 10x.
    # gen_2D_scatter(logger, split_col=1, x_col=13, y_col=9, split_mode='both', lin_reg_line=True)
    # ===================

    # 1. Resolution: 2x faster doing it with 1280 instead of 1920 for both Mpl and Pygame.
    # gen_2D_scatter(logger, split_col=1, x_col=2, y_col=9, split_mode='both', lin_reg_line=True)

    # 1. WRITE. Matplotlib: Massive overhead. Pygame: Overhead increase with increasing compute load.
    # gen_2D_scatter(logger[rows_mpl, :], split_col=5, x_col=13, y_col=9, split_mode='both', lin_reg_line=True, title='Matplotlib')
    # gen_2D_scatter(logger[rows_pygame, :], split_col=5, x_col=13, y_col=9, split_mode='both', lin_reg_line=True, title='Pygame')

    # 1. Computer
    # gen_2D_scatter(logger[rows_mpl, :], split_col=4, x_col=13, y_col=9, split_mode='both', lin_reg_line=True, title='Matplotlib')
    # gen_2D_scatter(logger[rows_pygame, :], split_col=4, x_col=13, y_col=9, split_mode='both', lin_reg_line=True, title='Pygame')

    # 1. RAM: Between 300-450 mb. Matplotlib uses about 15% more than Pygame.
    # gen_2D_scatter(logger, split_col=1, x_col=13, y_col=10, split_mode='both', lin_reg_line=True)

    # 1. Longer video = slower performance? Yes, but not too much to worry about.
    # gen_2D_scatter(logger[rows_only_largest, :], split_col=1, x_col=12, y_col=9, split_mode='only_high', lin_reg_line=True)
    # gen_2D_scatter(logger[rows_write, :], split_col=1, x_col=12, y_col=9, split_mode='only_low', lin_reg_line=True)  # mpl gets bad when writing long video.




    # 3D scatter ==============================================
    # Show both groups (default)
    # gen_3D_scatter(logger, split_col=1, x_col=6, y_col=7, z_col=9, split_mode='both')

    # Show only lower resolution (e.g., 1280x720)
    # gen_3D_scatter(logger, split_col=1, x_col=4, y_col=7, z_col=9, split_mode='only_high')

    # Show only higher resolution (e.g., 1920x1080)
    # gen_3D_scatter(logger, split_col=1, x_col=6, y_col=7, z_col=9, split_mode='only_high')

    plt.show()

# def gen_2D_scatter_old(logger, split_col, x_col, y_col, split_mode='both'):
#     fig, ax = plt.subplots()
#
#     color_map = {
#         0: 'red',
#         1: 'blue'
#     }
#
#     subset_data = subset_logger(logger, split_col, split_mode)
#
#     if isinstance(subset_data, dict):
#         for val, subset in subset_data.items():
#             ax.scatter(subset[:, x_col], subset[:, y_col],
#                        c=color_map[val], label=f"{split_col=}: {int(val)}")
#     else:
#         val = np.unique(subset_data[:, split_col])[0]
#         ax.scatter(subset_data[:, x_col], subset_data[:, y_col],
#                    c=color_map[val], label=f"{split_col=}: {int(val)}")
#
#     ax.set_xlabel(f"Column {x_col}")
#     ax.set_ylabel(f"Column {y_col}")
#     ax.set_title(f"2D Scatter Split by Column {split_col} ({split_mode})")
#     ax.legend()
#     plt.tight_layout()
#     plt.show()

