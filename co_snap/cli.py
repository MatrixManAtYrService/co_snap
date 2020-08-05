import argparse
import sys
from os import environ

# eval the output of this to supply necessary args
def init():
    print(
        """
       echo -n "User e-mail: "
       read CO_USER
       export CO_USER
       echo -n "Password: "
       read -s CO_PASSWORD
       export CO_PASSWORD"""
    )
    sys.exit(0)


# get stuff from sys.argv
def get_args(description):
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument("--url")
    parser.add_argument("--init", action="store_true")
    args = parser.parse_args()

    if args.init:
        init()

    try:
        args.user = environ["CO_USER"]
        args.password = environ["CO_PASSWORD"]
    except KeyError:
        print("CO_USER and CO_PASS not initialized", file=sys.stderr)
        print(f'try:\n\teval "$({path.abspath(__file__)} --init)"', file=sys.stdout)
        sys.exit(1)

    if args.url:
        return args

    else:
        print("pass --url or --init")


# prompt user
# default to yes
def yes_or_no(question):
    while "the answer is invalid":
        reply = str(input(question + " ([Y]/n): ")).lower().strip()
        if reply == "" or reply[0] in ["Y", "y"]:
            return True
        if reply[0] == "n":
            return False
