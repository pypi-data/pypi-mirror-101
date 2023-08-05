import sys
from pnplabs.main_entry_point import parse

if __name__ == '__main__':
    # print(f"Got: {sys.argv}")
    parse(user_args=sys.argv)
