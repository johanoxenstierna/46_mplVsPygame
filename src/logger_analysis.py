import numpy as np
import matplotlib.pyplot as plt
from typing import Literal

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


def gen_2D_scatter(logger, split_col, x_col, y_col, split_mode='both'):
    fig, ax = plt.subplots()

    color_map = {
        0: 'red',
        1: 'blue'
    }

    subset_data = subset_logger(logger, split_col, split_mode)

    if isinstance(subset_data, dict):
        for val, subset in subset_data.items():
            ax.scatter(subset[:, x_col], subset[:, y_col],
                       c=color_map[val], label=f"{split_col=}: {int(val)}")
    else:
        val = np.unique(subset_data[:, split_col])[0]
        ax.scatter(subset_data[:, x_col], subset_data[:, y_col],
                   c=color_map[val], label=f"{split_col=}: {int(val)}")

    ax.set_xlabel(f"Column {x_col}")
    ax.set_ylabel(f"Column {y_col}")
    ax.set_title(f"2D Scatter Split by Column {split_col} ({split_mode})")
    ax.legend()
    plt.tight_layout()
    plt.show()

def combine_features(logger, col6=6, col7=7, name='combined_feature'):
    """
    sqrt(avg_diam) * num_pngs
    col 6: num_pngs
    col 7: avg_diam
    col 13: combined
    """
    combined = logger[:, col6].astype(float) * np.sqrt(logger[:, col7].astype(float))
    combined = combined.reshape(-1, 1)
    logger_with_combined = np.hstack([logger, combined])
    return logger_with_combined

# Ready for new logger file to test updated combine_features behavior

if __name__ == '__main__':
    logger = np.load('./src/logger.npy')
    logger = logger[1:, :]  # Skip header
    logger = combine_features(logger)  # col 13: combined 6-7

    # 2D scatter =============================================
    gen_2D_scatter(logger, split_col=1, x_col=13, y_col=9, split_mode='both')
    adf = 5





    # 3D scatter ==============================================
    # Show both groups (default)
    # gen_3D_scatter(logger, split_col=1, x_col=6, y_col=7, z_col=9, split_mode='both')

    # Show only lower resolution (e.g., 1280x720)
    # gen_3D_scatter(logger, split_col=1, x_col=4, y_col=7, z_col=9, split_mode='only_high')

    # Show only higher resolution (e.g., 1920x1080)
    # gen_3D_scatter(logger, split_col=1, x_col=6, y_col=7, z_col=9, split_mode='only_high')

