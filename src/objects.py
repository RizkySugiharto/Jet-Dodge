import config
import random

class Obstacle:
    __objects = []

    def __init__(self, visual: str = "O"):
        self.__visual: str = visual[0]
        self.__position: list[int] = [random.randint(1, config.MAP_WIDTH - 2), config.MAP_HEIGHT + 1]

        Obstacle.__objects.append(self)

    def get_position(self) -> list[int]:
        return self.__position.copy()
    
    def get_visual_position(self) -> list[int]:
        x, y = self.__position.copy()
        max_x, max_y = config.MAP_WIDTH - 1, config.MAP_HEIGHT

        if x < 1:
            x = 1
        elif x > max_x:
            x = max_x

        if y < 1:
            y = 1
        elif y > max_y:
            y = -1

        return [x, y]
    
    def get_visual(self) -> str:
        return self.__visual
    
    def update_position(self):
        self.__position[1] -= 1

    @staticmethod
    def get_obstacles() -> list[object]:
        return Obstacle.__objects
    
    @staticmethod
    def remove(obstacle: object):
        Obstacle.__objects.remove(obstacle)

    @staticmethod
    def remove_all():
        Obstacle.__objects.clear()

class Player:
    def __init__(self, visual: str = "$", position: list[int] = [(config.MAP_WIDTH // 2), 1]):
        self.__visual: str = visual[0]
        self.__position: list[int] = position
        self.__moving: list[int] = [0, 0]

    def move(self, distance_x: int = 0, distance_y: int = 0):
        map_border = {
            'x': {'left': 0, 'right': (config.MAP_WIDTH - 1)},
            'y': {'top': 0, 'bottom': config.MAP_HEIGHT + 1}
        }
        new_position = [self.__position[0] + distance_x, self.__position[1] + distance_y]

        if new_position[0] in map_border['x'].values() or new_position[1] in map_border['y'].values():
            return
        
        self.__position = new_position
        self.__moving = [distance_x, distance_y]

    def normalize_moving(self):
        self.__moving = [0, 0]

    def get_position(self) -> list[int]:
        x, y = self.__position
        moving_x, moving_y = self.__moving

        return [x, y]
    
    def get_visual(self) -> str:
        return self.__visual