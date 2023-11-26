# The maximum size of the playing area width
MAP_WIDTH: int = 8

# The maximum size of the playing area height
MAP_HEIGHT: int = 20

# Minimum distance between obstacles
# The distance should not be more than the height of the playing area
# Not allowed --> ( MINIMAL_OBSTACLES_RANGE < MAP_HEIGHT )
MINIMAL_OBSTACLES_RANGE: int = 3

# Maximum number of fps in the game
# If you don't want to limit fps in the game, set the value to less than zero, for example: -1
MAX_FPS: int = 15

# The maximum number of obstacles that will be given in the game
MAX_OBSTACLE: int = 7