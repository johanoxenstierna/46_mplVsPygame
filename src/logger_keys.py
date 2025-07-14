# logger_keys.py

logger_keys = {
    0: "Experiment #",
    1: ("Backend", {0: "Matplotlib", 1: "Pygame"}),
    2: "Resolution", # 1280 vs 1920
    3: "FPS", # 60, 100, 144
    4: ("Computer", {0: "Laptop", 1: "Workstation"}),
    5: ("WRITE", {0: "No", 1: "Yes"}),  # prebuild first 100 filenames
    6: "# PNGs",
    7: "PNG Avg. Diameter (px)",
    8: "# Dots",
    9: "Perf Time (sec per 60s)",
    10: "RAM (MB)",
    11: "Visual Quality",
    12: "Num Frames",
    13: "Compute Load"  # combination of features 6-7
}
