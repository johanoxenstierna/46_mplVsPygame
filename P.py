
MPL0PYGAME1 = None  # set in main

'''These are dimensions for backr pic. Has a huge impact on cpu-time'''

# MAP_DIMS = (1280, 720)
MAP_DIMS = (1920, 1080)
# MAP_DIMS = (2560, 1440)

FRAMES_START = 0
FRAMES_STOP = 3600  #30000  OBS: Will be bugs if lower than, say, 4000
FRAMES_TOT_BODIES = FRAMES_STOP - 25
FRAMES_TOT = FRAMES_STOP - FRAMES_START

FPS = 100  # 17:31
SPEED_MULTIPLIER = 0.4  #latest: 0.4
WRITE = 0  # OBS USE CORRECT NUMBER
SAVE = 1
REAL_SCALE = 0

OBJ_TO_SHOW = []
OBJ_TO_SHOW.append('Calidus')  # JUST USE ALPHA in main
OBJ_TO_SHOW.append('Ogun')
OBJ_TO_SHOW.append('Venus')
OBJ_TO_SHOW.append('Nauvis')
OBJ_TO_SHOW.append('GSS')
OBJ_TO_SHOW.append('Molli')
OBJ_TO_SHOW.append('Mars')
OBJ_TO_SHOW.append('Astro0')
OBJ_TO_SHOW.append('Astro0b')
OBJ_TO_SHOW.append('Jupiter')
OBJ_TO_SHOW.append('Everglade')
OBJ_TO_SHOW.append('Petussia')
OBJ_TO_SHOW.append('Saturn')
OBJ_TO_SHOW.append('Uranus')
OBJ_TO_SHOW.append('Neptune')
OBJ_TO_SHOW.append('Rockets')
# OBJ_TO_SHOW.append('YearsDays')

VID_SINGLE_WORD = '_'
for word in OBJ_TO_SHOW:
    VID_SINGLE_WORD += word[0] + '_'

