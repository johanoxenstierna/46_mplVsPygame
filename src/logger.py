
import psutil
import os
import numpy as np

import P


class Logger:
    def __init__(_s, o0calidus, R):

        '''
        RESULT ARRAY
        0 Experiment num
        1 Backend
        2 Resolution
        3 FPS
        4 Computer (0=laptop, 1=wrkstn)
        5 WRITE  (if not 0, it also specifies an enumerated file-name - that can then be used to fill in visual quality)
        6 Num. png's
        7 Avg. pixels shown of png's during animation
        8 Num. dots.
        9 perf_time (sec to generate 1 min)
        10 RAM
        11 VisQuality (manual)
        12 NUM_FRAMES

        NOT INCLUDED IN ARRAY (bcs its subjective/no need for precision and will be discussed instead)
        Ease of use
        Blit (assumed always used)
        '''

        _s.logger = np.load('./src/logger.npy')
        experiment_num = len(_s.logger) - 1
        _s.row = [
            experiment_num,
            P.MPL0PYGAME1,
            P.MAP_DIMS[0],
            P.FPS,
            1,
            P.WRITE,
            999,
            999,
            999,
            999,
            999,
            999,
            P.FRAMES_TOT
        ]

        _s.get_info(o0calidus, R)

        print(_s.logger)
        print(np.asarray(_s.row))

    def get_info(_s, o0calidus, R):

        num_pngs = len(o0calidus.O1) - 2
        png_diam = []
        num_dots = 0
        if R is not None:
            num_dots = len(R)

        for o1_id, o1 in o0calidus.O1.items():
            if o1.type == '0_static':
                continue
            elif o1.type == '0_':
                diam = int(2 * o1.centroids[0])
                png_diam.append(diam)
            elif o1.type == 'body':
                diam = int(np.mean(2 * o1.centroids))
                png_diam += [diam, diam, diam]
            elif o1.type == 'astro':
                x = 1080 * 1.3
                y = 1080 * 0.25
                diam = int(0.5 * (x + y))
                png_diam.append(diam)

        _s.row[6] = num_pngs
        _s.row[7] = int(np.mean(png_diam))
        _s.row[8] = num_dots

    def get_ram_usage_mb(_s):
        process = psutil.Process(os.getpid())
        RAM_USAGE = process.memory_info().rss // 1024 ** 2  # in MB
        # print("RAM_USAGE: " + str(RAM_USAGE))
        _s.row[10] = int(RAM_USAGE)

    def add_save(_s):
        # logger = np.load('./src/logger.npy')
        row = np.asarray(_s.row)
        logger = np.vstack([_s.logger, row])
        print(logger)
        np.save('./src/logger.npy', logger)


if __name__ == "__main__":
    """
    THIS IS WHERE MANUAL THINGS WILL BE ENTERED FOR THE ARRAY
    OBS COMMENT OUT
    """

    # First time save  OBS COMMENT OUT
    # logger = np.zeros((1, 11), dtype=int)
    # logger = np.array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10], dtype=int)
    # np.save('./src/logger.npy', logger)

    # Delete rows ============
    logger = np.load('./src/logger.npy')
    adsf = 5
    rows_to_delete = [19]
    # rows_to_delete = np.argwhere(logger[:, 4] == 7)
    logger = np.delete(logger, rows_to_delete, axis=0)
    # np.save('./src/logger.npy', logger)

    # Add col: =================
    # logger = np.load('./src/logger.npy')
    # # col = np.array([11, 400, 400, 1800, 400])
    # col = np.array([0, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16])[:, np.newaxis]
    # # col = col[:, np.newaxis]
    # # logger = np.hstack(([logger, col]))
    # logger = np.hstack(([col, logger]))
    # logger[0, :] = np.array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12])
    # adsf = 5
    # np.save('./src/logger.npy', logger)

    pass
