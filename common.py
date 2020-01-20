import os

SIZE = 1024
STEP = SIZE // 8
FLIP_COUNT_MAX = 20

RANKS = [ letter for letter in 'abcdefgh' ]
FILES = list(range(1,9))

APP_DIR = os.path.dirname(os.path.abspath(__file__))
RESOURCE_DIR = os.path.join(APP_DIR,'resources')

print('resource_dir',RESOURCE_DIR)
BOARD_WHITE_FILENAME = os.path.join(RESOURCE_DIR, 'board-white-2048.png')
BOARD_BLACK_FILENAME = os.path.join(RESOURCE_DIR, 'board-black-2048.png')

DATA_DIR = os.path.join(APP_DIR,'data')

if not os.path.exists(DATA_DIR):
    print('creating:',DATA_DIR)
    os.makedirs(DATA_DIR)

STATS_FILENAME = os.path.join(DATA_DIR,'stats.pkl')

SQUARE_TO_LOCATION = {}
LOCATION_TO_SQUARE = {}

for x in range(8):
    for y in range(8):
        location = (x,y)
        square = '{}{}'.format(RANKS[x],FILES[y])
        LOCATION_TO_SQUARE[location] = square
        SQUARE_TO_LOCATION[square] = location
