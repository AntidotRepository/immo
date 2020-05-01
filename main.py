import argparse
from Model.DB.db import *
from Controller.controller import *

"""MVC example:
https://gist.github.com/ajfigueroa/c2af555630d1db3efb5178ece728b017"""

if __name__ == "__main__":   
    parser = argparse.ArgumentParser()

    parser.add_argument('-f', '--filter', help="Filter offer")
    parser.add_argument('-c', '--comment', help="Comments")
    parser.add_argument('-p', '--parse', help="Start parse", action="store_true")

    args = parser.parse_args()

    if args.filter:
        print("offer {}".format(args.filter))
    if args.comment:
        print("comments: {}".format(args.comment))

    if not args.filter and not args.comment:
        if args.parse:
            print("start app with parsing")
            skip = False
        else:
            print("Skip parsing")
            skip = True
        my_controller = Controller(fake=False, skip_parse=skip)
    else:
        if args.comment and not args.filter:
            print("-f option needed")
        else:
            my_db = DB()
            my_db.filter_offer(args.filter)
            if args.comment:
                my_db.comment_offer(args.filter, args.comment)
            my_db.close()
