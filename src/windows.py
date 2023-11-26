from abc import ABC, abstractmethod
from fps import Fps
from functools import wraps
from objects import Player, Obstacle
from typing_extensions import override
import colorama
import config
import keyboard
import os
import status
import random
import time

colorama.init(autoreset=True)

def always_clear(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        os.system("cls")
        result = func(*args, **kwargs)

        return result

    return wrapper

class BaseWindow(ABC):
    def __init__(self):
        printed_list = []
        self.__printed_text = "\n".join(printed_list)

    @abstractmethod
    def apply_and_update(self) -> bool:
        print(self.__printed_text)

        return True

class Menu(BaseWindow):
    def __init__(self):
        self.__printed_text = ""
        self.__highlight_text = 2
        self.__has_select = False
        self.__quit = False

        self.update_display()

    @override
    @always_clear
    def apply_and_update(self):
        self.update_display()
        self.listen_keyboard_event()

        print(self.__printed_text)

        return not self.__quit
    
    def new_window(self) -> bool:
        return self.__has_select
    
    def reset(self):
        self.__printed_text = ""
        self.__highlight_text = 2
        self.__has_select = False
        self.__quit = False

    def move_selected_text(self, range_move: int):
        MINIMUM_VALUE = 2
        MAXIMUM_VALUE = 3

        selectable_value = self.__highlight_text + range_move

        if selectable_value < MINIMUM_VALUE or selectable_value > MAXIMUM_VALUE:
            return
        
        self.__highlight_text = selectable_value

    def listen_keyboard_event(self):
        if keyboard.is_pressed("w") or keyboard.is_pressed("up"):
            self.move_selected_text(range_move=(-1))
        elif keyboard.is_pressed("s") or keyboard.is_pressed("down"):
            self.move_selected_text(range_move=(1))
        elif keyboard.is_pressed("enter"):
            match self.__highlight_text:
                case 2:
                    self.__has_select = True
                    self.__quit = False
                case 3:
                    self.__has_select = True
                    self.__quit = True

    def update_display(self):
        printed_list = [
            "-- Jet Dodge --",
            "",
            "> Start",
            "> Quit",
            "",
            "---------------"
        ]
        printed_list[self.__highlight_text] = colorama.Back.WHITE + printed_list[self.__highlight_text] + colorama.Back.RESET

        self.__printed_text = "\n".join(printed_list)

class Gameplay(BaseWindow):
    def __init__(self):
        self.__visual: str = ("|" + (" " * (config.MAP_WIDTH - 2)) + "|" + "\n") * config.MAP_HEIGHT
        self.__visual_default: str = self.__visual
        self.__player: Player = Player()
        self.__current_obstacles: int = len(Obstacle.get_obstacles())
        self.__range_per_obstacles: int = config.MINIMAL_OBSTACLES_RANGE
        self.__current_range_per_obstacles: int = self.__range_per_obstacles
        self.__fps = Fps()
        self.__status = status.PLAYING
        self.__is_over = False

        self.update_range_per_obstacles()
        self.refresh_visual()

    @override
    def apply_and_update(self) -> bool:
        start_time = time.time()

        self.update_display()

        try:
            if keyboard.is_pressed("q"):
                self.__status = status.STOPPED
                return False
        except:
            return False

        self.listen_events()
        self.__is_over = self.update_obstacles()
        self.__player.normalize_moving()

        self.__status = status.GAME_OVER if self.__is_over else status.PLAYING

        self.refresh_visual()
        self.__fps.update(start_time=start_time)

        return True
    
    def is_over(self) -> bool:
        return self.__is_over

    @always_clear
    def update_display(self):
        print(f"{'Jet Dodge': ^{config.MAP_WIDTH}}")
        print(f"{f'[{self.__status}]': ^{config.MAP_WIDTH}}")
        print(f"FPS: {self.__fps.get()}")
        print()
        print(self.get_visual())
        print()
        print("Press 'q' to quit the game")

    def reset(self):
        Obstacle.remove_all()

        self.__visual = self.__visual_default
        self.__player = Player()
        self.__current_obstacles = len(Obstacle.get_obstacles())
        self.__range_per_obstacles = config.MINIMAL_OBSTACLES_RANGE
        self.__current_range_per_obstacles = self.__range_per_obstacles
        self.__fps = Fps()
        self.__status = status.PLAYING
        self.__is_over = False

        self.update_range_per_obstacles()
        self.refresh_visual()

    def get_player(self) -> Player:
        return self.__player
    
    def get_visual(self) -> str:
        return self.__visual
    
    def get_obstacles_count(self) -> int:
        return self.__current_obstacles
    
    def update_range_per_obstacles(self):
        self.__range_per_obstacles = random.randint(
            config.MINIMAL_OBSTACLES_RANGE,
            config.MAP_HEIGHT - config.MINIMAL_OBSTACLES_RANGE
        )
    
    def update_obstacles(self) -> bool:
        obstacles = Obstacle.get_obstacles()
        is_over = False

        for obstacle in obstacles:
            if self.__player.get_position() == obstacle.get_position(): # type: ignore
                is_over = True

            obstacle.update_position() # type: ignore

            if self.__player.get_position() == obstacle.get_position(): # type: ignore
                is_over = True

            if obstacle.get_position()[1] <= 0: # type: ignore
                Obstacle.remove(obstacle)
                self.__current_obstacles -= 1

        if self.__current_range_per_obstacles >= self.__range_per_obstacles:
            if self.__current_obstacles < config.MAX_OBSTACLE:
                Obstacle()
                self.__current_obstacles += 1

            self.__current_range_per_obstacles = 0
            
            self.update_range_per_obstacles()
        else:
            self.__current_range_per_obstacles += 1


        return is_over
    
    def refresh_visual(self):
        player_x, player_y = self.__player.get_position()
        player_visual = self.__player.get_visual()
        obstacles = Obstacle.get_obstacles()

        map_visual_list = self.__visual_default.splitlines()        
        changed_visual = map_visual_list[player_y - 1]

        map_visual_list[player_y - 1] = changed_visual[:player_x] + player_visual + changed_visual[(player_x + 1):]

        for obstacle in obstacles:
            obstacle_x, obstacle_y = obstacle.get_visual_position() # type: ignore

            if obstacle_y == -1:
                continue

            obstacle_visual = obstacle.get_visual() # type: ignore
            map_visual_list[obstacle_y - 1] = changed_visual[:obstacle_x] + obstacle_visual + changed_visual[(obstacle_x + 1):]

        self.__visual = "\n".join(map_visual_list)

    def listen_events(self):
        try:
            if keyboard.is_pressed("d") or keyboard.is_pressed("right"):
                self.__player.move(distance_x=1)
            elif keyboard.is_pressed("a") or keyboard.is_pressed("left"):
                self.__player.move(distance_x=-1)
            elif keyboard.is_pressed("w") or keyboard.is_pressed("up"):
                self.__player.move(distance_y=-1)
            elif keyboard.is_pressed("s") or keyboard.is_pressed("down"):
                self.__player.move(distance_y=1)
        except:
            pass

class TryAgain(BaseWindow):
    def __init__(self, gameplay_window: Gameplay):
        self.__game_play = gameplay_window
        self.__printed_text = ""
        self.__highlight_text = 7
        self.__quit = False
        self.__new_gameplay = False

    @override
    def apply_and_update(self) -> bool:
        self.update_display()
        self.listen_keyboard_event()

        print(self.__printed_text)

        return not self.__quit

    @always_clear
    def update_display(self):
        printed_list = [
            f"{'Jet Dodge': ^{config.MAP_WIDTH}}",
            f"{f'[{status.GAME_OVER}]': ^{config.MAP_WIDTH}}",
            "FPS: 1",
            "",
            self.__game_play.get_visual(),
            "",
            "Do you want to try again?",
            "> YES",
            "> NO "
        ]
        printed_list[self.__highlight_text] = colorama.Back.WHITE + printed_list[self.__highlight_text] + colorama.Back.RESET

        self.__printed_text = "\n".join(printed_list)

    def new_gameplay(self) -> bool:
        return self.__new_gameplay

    def move_selected_text(self, range_move: int):
        MINIMUM_VALUE = 7
        MAXIMUM_VALUE = 8

        selectable_value = self.__highlight_text + range_move

        if selectable_value < MINIMUM_VALUE or selectable_value > MAXIMUM_VALUE:
            return
        
        self.__highlight_text = selectable_value

    def listen_keyboard_event(self):
        if keyboard.is_pressed("w") or keyboard.is_pressed("up"):
            self.move_selected_text(range_move=(-1))
        elif keyboard.is_pressed("s") or keyboard.is_pressed("down"):
            self.move_selected_text(range_move=(1))
        elif keyboard.is_pressed("enter"):
            match self.__highlight_text:
                case 7:
                    self.__new_gameplay = True
                    self.__quit = False
                    self.__game_play.reset()
                case 8:
                    self.__new_gameplay = False
                    self.__quit = True

