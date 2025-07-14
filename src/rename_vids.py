
import os
import shutil
from pathlib import Path
import numpy as np

PATH_IN = Path('./vids/')
PATH_OUT = Path('./vids_2/')

_, _, file_names_fold = os.walk('./vids/').__next__()
logger = np.load('./src/logger.npy')
logger = logger[1:, :]

for i in range(len(logger)):
    name_vid_logger = str(logger[i, 5])
    if name_vid_logger == '0':
        continue

    for j in range(len(file_names_fold)):
        name_vid_fold_0 = file_names_fold[j]  # file_name
        name_vid_fold_1 = name_vid_fold_0.split('_')
        name_vid_fold_2 = name_vid_fold_1[1]

        if name_vid_fold_2 == name_vid_logger:

            bcknd = logger[i, 1]
            if bcknd == 0:
                bcknd = 'mpl'
            else:
                bcknd = 'pyg'

            res = str(logger[i, 2])
            fps = str(logger[i, 3])
            perf_time = str(logger[i, 9])
            name_new = 'vid_' + name_vid_fold_2 + '_' + bcknd + '_' + res + '_' + fps + '_' + perf_time + '.mp4'

            original_file = PATH_IN / name_vid_fold_0
            temp_copy = PATH_IN / name_new
            shutil.copy2(original_file, temp_copy)
            shutil.move(temp_copy, PATH_OUT / temp_copy.name)

            adf = 6

    adf = 5

adf = 5