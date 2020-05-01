import argparse
from Model.DB.db import *
from Controller.controller import *

"""MVC example:
https://gist.github.com/ajfigueroa/c2af555630d1db3efb5178ece728b017"""

if __name__ == "__main__":   
    parser = argparse.ArgumentParser()

    parser.add_argument('-f', '--filter', help="Filter offer")
    parser.add_argument('-c', '--comment', help="Comments")

    args = parser.parse_args()

    if args.filter:
        print("offer {}".format(args.filter))
    if args.comment:
        print("comments: {}".format(args.comment))


    #my_controller = Controller(fake=False, skip_parse=True)
