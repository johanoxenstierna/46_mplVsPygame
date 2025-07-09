
import numpy as np
import matplotlib.pyplot as plt

def gen_3D_scatter(logger, split_col, x_col, y_col, z_col, split_mode='both'):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    unique_vals = np.unique(logger[:, split_col])
    if len(unique_vals) != 2:
        raise ValueError(f"Expected exactly 2 unique values in split_col {split_col}, got {unique_vals}")

    val_low, val_high = sorted(unique_vals)
    color_map = {
        val_low: 'red',
        val_high: 'blue',
    }

    if split_mode == 'both':
        for val in unique_vals:
            subset = logger[logger[:, split_col] == val]
            ax.scatter(
                subset[:, x_col], subset[:, y_col], subset[:, z_col],
                c=color_map[val],
                label=f"{split_col=}: {int(val)}"
            )
    elif split_mode == 'only_low':
        subset = logger[logger[:, split_col] == val_low]
        ax.scatter(subset[:, x_col], subset[:, y_col], subset[:, z_col],
                   c=color_map[val_low], label=f"{split_col=}: {int(val_low)}")
    elif split_mode == 'only_high':
        subset = logger[logger[:, split_col] == val_high]
        ax.scatter(subset[:, x_col], subset[:, y_col], subset[:, z_col],
                   c=color_map[val_high], label=f"{split_col=}: {int(val_high)}")
    else:
        raise ValueError(f"Invalid split_mode '{split_mode}'. Choose 'both', 'only_low', or 'only_high'.")

    ax.set_xlabel(f"Column {x_col}")
    ax.set_ylabel(f"Column {y_col}")
    ax.set_zlabel(f"Column {z_col}")
    ax.set_title(f"3D Scatter Split by Column {split_col} ({split_mode})")
    ax.legend()
    plt.tight_layout()
    plt.show()


if __name__ == '__main__':
    logger = np.load('./src/logger.npy')
    logger = logger[1:, :]  # Skip header

    # Show both groups (default)
    # gen_3D_scatter(logger, split_col=1, x_col=6, y_col=7, z_col=9, split_mode='both')

    # Show only lower resolution (e.g., 1280x720)
    gen_3D_scatter(logger, split_col=1, x_col=4, y_col=7, z_col=9, split_mode='only_high')

    # Show only higher resolution (e.g., 1920x1080)
    # gen_3D_scatter(logger, split_col=1, x_col=6, y_col=7, z_col=9, split_mode='only_high')
