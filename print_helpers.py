"""Print Helper Module."""
import random


class PrintHelper:
    RAINBOW_COLORS = [
        "\033[41m",  # Red
        "\033[43m",  # Yellow
        "\033[42m",  # Green
        "\033[46m",  # Cyan
        "\033[44m",  # Blue
        "\033[45m",  # Magenta
    ]
    BOLD = "\033[1m"
    RESET = "\033[0m"  # Reset styling
    WHITE = "\033[1;97m\033[1m"  # "\033[1;97m"

    @classmethod
    def print_welcome_msg(cls):
        """Method to print a welcome message."""
        welcome_lines = [
            "                   __O           ",
            "                  / /\\_,         Welcome",
            "                ___/\\                   To",
            "                    /_                     Wikisaver",
            "                                                       __O          ",
            "                                                      / /\\_,        Welcome",
            "                                                    ___/\\                  To",
            "                                                        /_                    Wikisaver",
        ]

        welcome = "\n".join(
            f"{random.choice(cls.RAINBOW_COLORS)}{cls.WHITE}{cls.BOLD}{line}{cls.RESET}" for line in welcome_lines)

        print(welcome)

    @classmethod
    def print_seperator(cls):
        sep =  "\t\t\t\t\t\t\t\t\t\t\t"
        print( f"{random.choice(cls.RAINBOW_COLORS)}{sep}{cls.RESET}")

    @classmethod
    def pr_menu(cls, txt):
        """Prints the Menu items in teal color."""
        print("\033[38;5;37m" + txt + "\033[0m")

    @classmethod
    def pr_error(cls, txt):
        """Print error messages in red"""
        print("\033[91m" + txt + "\033[0m")

    @classmethod
    def pr_bold(cls, txt):
        """Prints text in bold"""
        print("\033[1m" + txt + "\033[0m")


    @classmethod
    def pr_input(cls, txt):
        """Print input prompt in a brownish color (yellow)"""
        return input("\033[33m" + txt + "\033[0m").strip()
