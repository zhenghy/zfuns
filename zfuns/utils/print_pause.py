from pprint import pprint


def print_pasue(*args) -> None:
    """Print args and pause"""
    if len(args) == 1:
        pprint(args[0])
    else:
        for arg in args:
            pprint(arg)

    if input("continue? Y/N") != "Y":
        exit(1)
