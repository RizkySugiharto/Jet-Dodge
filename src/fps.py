import time
import config

class Fps:
    def __init__(self):
        self.__fps: int = 0
        self.__max_time: float = (1 / config.MAX_FPS) if config.MAX_FPS > 0 else -1

    def update(self, start_time: float):
        try:
            end_time = time.time()
            calculated_time = end_time - start_time

            if calculated_time < self.__max_time:
                time.sleep(self.__max_time - calculated_time)

                self.__fps = int(1 / self.__max_time)

                return
            
            self.__fps = int(1 / (end_time - start_time))
        except ZeroDivisionError:
            self.__fps = 0

    def get(self) -> int:
        return self.__fps