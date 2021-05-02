def output(string, color):
    return color + str(string) + BColors.ENDC


def test_colors():
    print(BColors.BOLD + "BOLD" + BColors.ENDC)
    print(BColors.UNDERLINE + "UNDERLINE" + BColors.ENDC)
    print(BColors.BLACK + "BLACK" + BColors.ENDC)
    print(BColors.RED + "RED" + BColors.ENDC)
    print(BColors.GREEN + "GREEN" + BColors.ENDC)
    print(BColors.YELLOW + "YELLOW" + BColors.ENDC)
    print(BColors.BLUE + "BLUE" + BColors.ENDC)
    print(BColors.PURPLE + "PURPLE" + BColors.ENDC)
    print(BColors.CYAN + "CYAN" + BColors.ENDC)
    print(BColors.LIGHT_GRAY + "LIGHT_GRAY" + BColors.ENDC)
    print(BColors.DARK_GRAY + "DARK_GRAY" + BColors.ENDC)
    print(BColors.LIGHT_RED + "LIGHT_RED" + BColors.ENDC)
    print(BColors.LIGHT_GREEN + "LIGHT_GREEN" + BColors.ENDC)
    print(BColors.LIGHT_YELLOW + "LIGHT_YELLOW" + BColors.ENDC)
    print(BColors.LIGHT_BLUE + "LIGHT_BLUE" + BColors.ENDC)
    print(BColors.LIGHT_PURPLE + "LIGHT_PURPLE" + BColors.ENDC)
    print(BColors.LIGHT_CYAN + "LIGHT_CYAN" + BColors.ENDC)
    print(BColors.WHITE + "WHITE" + BColors.ENDC)


class BColors:
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"
    BLACK = "\033[30m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    PURPLE = "\033[35m"
    CYAN = "\033[36m"
    LIGHT_GRAY = "\033[37m"
    DARK_GRAY = "\033[90m"
    LIGHT_RED = "\033[91m"
    LIGHT_GREEN = "\033[92m"
    LIGHT_YELLOW = "\033[93m"
    LIGHT_BLUE = "\033[94m"
    LIGHT_PURPLE = "\033[95m"
    LIGHT_CYAN = "\033[96m"
    WHITE = "\033[97m"
