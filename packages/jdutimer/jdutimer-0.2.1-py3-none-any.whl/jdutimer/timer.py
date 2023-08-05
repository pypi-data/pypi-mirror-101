import time
from jdutimer.display import color, warning, info, error


class Singleton(type):
    """
    Singleton class to inherit from to create a new singleton.
    """
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(
                Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Timer(metaclass=Singleton):
    """
    Class made to measure execution time easily, and get a summary of all measurements.
    """

    def __init__(self):
        """
        Initialisation class for timer.
        """

        self.funcs = []         # list of block functions
        self.titles = []        # list of block titles
        self.__subfuncs = []    # current block functions
        self.__blocktimes = []  # list of total block time in ms

    def add(self, func, *args):
        """
        Get function execution time, and adds it to an array for later use.
        For display, call pack() then print_block() or final_print().
        """

        start_time = time.time()
        ret = func(*args)
        end_time = time.time()

        self.__subfuncs.append((func.__name__, end_time - start_time))

        return ret

    def pack(self, title):
        """
        Takes current timed functions results and stores it as a block with a given title. For display, call print_block() or final_print().
        """

        self.titles.append(title)
        self.funcs.append(self.__subfuncs)

        self.__blocktimes.append(sum([t for (_, t) in self.__subfuncs]))
        self.__subfuncs = []

    def show_block(self, id=-1, unit="ms"):
        """
        Prints block with given id. id can be an integer or the name of the block.
        """

        if isinstance(id, str):
            id = self.__find_block(id)

        if isinstance(id, int):
            try:
                l_func = self.__longest_func()
                for func, time in self.funcs[id]:
                    self.__print(" ", func, time, 0, l_func, unit)
            except:
                error("id out of range.")

    def show(self, unit="ms"):
        """
        Prints all blocks, with title, and inner functions execution time.
        """

        l_func = self.__longest_func()
        l_title = self.__longest_title()

        for i, (b_func, title) in enumerate(self.__summary()):
            self.__print(title, "", 0, l_title, 0, unit, color.BOLD)

            for func, time in b_func:
                self.__print(" ", func, time, l_title, l_func, unit)

            self.__print("", " ", self.__blocktimes[i],
                         l_title, l_func, unit, tag=color.GREEN)

        self.__print("", '-' * l_func, 0, l_title, l_func, unit)
        self.__print("", "TOTAL", sum(self.__blocktimes),
                     l_title, l_func, unit, color.BOLD + color.GREEN)

        if len(self.__subfuncs) != 0:
            warning(
                f"\nsome timed functions are not packed yet.\nCall {self.__name()}().pack() to stack them.")
            self.__print("UNPACKED", "", 0, l_title, 0, unit, color.BOLD)

            for func, time in self.__subfuncs:
                self.__print(" ", func, time, l_title, l_func, unit)

    def rename(self, old, new):
        """
        Rename a given block. old can be the index of the block, or its name.
        """
        assert isinstance(new, str), "second argument has to be a string."

        if isinstance(old, str):
            old = self.__find_block(old)

        if isinstance(old, int):
            try:
                self.titles[old] = new
            except:
                error("id out of range.")

    def __find_block(self, id):
        try:
            return self.titles.index(id)
        except:
            error(f"timer block '{id}' not found.")
            return None

    def __print(_, str1, str2, time, len1, len2, unit, tag=color.END):
        """
        Inner-class print format method.
        """

        string = f"{str2:<{len2}}"

        if len1 != 0:
            string = f"{str1:<{len1+1}}" + string

        if time != 0:
            if unit == "ms":
                time *= 1000
            if unit == "cs":
                time *= 100
            if unit == "ds":
                time *= 10
            if unit == "s":
                time *= 1

            string = string + " " * 3 + f"{time:7.2f}{unit}"

        print(tag + string + color.END)

    def __summary(self):
        """
        Inner-class to zip all block related attributes.
        """

        return zip(self.funcs, self.titles)

    def __name(self):
        """
        Proxy for class name.
        """

        return self.__class__.__name__

    def __longest_func(self):
        max_l = 0
        for b_func in self.funcs:
            for f, _ in b_func:
                max_l = len(f) if len(f) > max_l else max_l

        if max_l < 5:
            return 5

        return max_l

    def __longest_title(self):
        """
        Get the length of the longest function.
        """

        return len(max(self.titles, key=len))

    def __str__(self):
        """
        Short instance description.
        """

        strings = []
        strings.append(
            f"{self.__name()} class with {len(self.titles)} blocks packed:")

        for b_func, title in self.__summary():
            strings.append(f"\t- {title} ({', '.join(b_func[0])})")

        return '\n'.join(strings)
