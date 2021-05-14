# Local application imports
from .bcolors import output
from .bcolors import BColors


def log(message, level=""):
    level = level.lower()
    level_color = None
    if level in ["critical", "error"]:
        level_color = BColors.RED
    if level in ["warning"]:
        level_color = BColors.LIGHT_YELLOW
    elif level in ["info"]:
        level_color = BColors.LIGHT_BLUE

    level = level.capitalize()
    if level_color:
        print("[{level}]: {message}".format(level=output(level, level_color), message=message))
    elif level != "":
        print("[{level}]: {message}".format(level=level, message=message))
    else:
        print("{message}".format(message=message))


def log_info(message):
    log(message, "info")


def log_success(message):
    log_info(output(message, BColors.GREEN))


def log_warning(message):
    log(message, "warning")


def log_error(message):
    log(message, "error")
