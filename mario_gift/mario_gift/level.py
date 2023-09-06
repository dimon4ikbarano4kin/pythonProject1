import platform

FILE = "./levels/1.txt"
BG_FILE = "./images/bg.gif"


class Level:
    path_level: str

    def __init__(self, path=FILE):
        self.path_level = path
        self.platforms = []
        self.__lines_of_file = []
        self.__load()
        self.__get_platform()
        self.width = len(self.__lines_of_file[0]) * platform.PLATFORM_WIDTH
        self.height = len(self.__lines_of_file) * platform.PLATFORM_HEIGHT

    def __load(self):
        with open(self.path_level, "r", encoding="utf-8") as file:
            for line in file:
                self.__lines_of_file.append(line[:-1])

    def __get_platform(self):
        x = y = 0
        for line in self.__lines_of_file:
            for symbol in line:
                if symbol == '-':
                    pf = platform.Platform(x, y)
                    self.platforms.append(pf)
                elif symbol == "*":
                    pf = platform.DieBlock(x, y)
                    self.platforms.append(pf)
                x += platform.PLATFORM_WIDTH

            y += platform.PLATFORM_HEIGHT
            x = 0
