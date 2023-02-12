''' ARENA SETTINGS '''
GRID_LENGTH = 200
GRID_CELL_LENGTH = 10
SCALING_FACTOR = 3
INITPOS = ((GRID_LENGTH // GRID_CELL_LENGTH) - 1, 0, "N")

BUTTON_LENGTH = 100
BUTTON_WIDTH = 30

''' ROBOT SETTINGS '''
ROBOT_LENGTH = 30
ROBOT_WIDTH = 30


''' COLOUR SETTINGS '''
RED = (242, 0, 0)
GREEN = (26, 255, 0)
BLUE = (6, 46, 250)

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREY = (163, 163, 194)

PINK = (255, 51, 255)
ORANGE = (255, 154, 0)
YELLOW = (255, 255, 18)
LIGHT_BLUE = (1, 255, 255)

# Robot Attributes
ROBOT_LENGTH = 20 * SCALING_FACTOR
ROBOT_TURN_RADIUS = 30 * SCALING_FACTOR
ROBOT_SPEED_PER_SECOND = 100 * SCALING_FACTOR
ROBOT_S_FACTOR = ROBOT_LENGTH / ROBOT_TURN_RADIUS  # Please read briefing notes from Imperial
ROBOT_SAFETY_DISTANCE = 15 * SCALING_FACTOR
ROBOT_SCAN_TIME = 0.25  # Time provided for scanning an obstacle image in seconds.

# Grid Attributes
GRID_LENGTH = 200 * SCALING_FACTOR
GRID_CELL_LENGTH = 10 * SCALING_FACTOR
GRID_START_BOX_LENGTH = 30 * SCALING_FACTOR
GRID_NUM_GRIDS = GRID_LENGTH // GRID_CELL_LENGTH

