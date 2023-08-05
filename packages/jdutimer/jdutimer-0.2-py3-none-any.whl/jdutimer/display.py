class color:
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    DARKCYAN = '\033[36m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'


def warning(str):
    """
    Prints string in yellow.
    """

    print(color.YELLOW + f"Warning: {str}" + color.END)


def error(str):
    """
    Prints string in red.
    """

    print(color.RED + f"Error: {str}" + color.END)


def info(str):
    """
    Prints string in blue.
    """

    print(color.BLUE + f"Info: {str}" + color.BLUE)
