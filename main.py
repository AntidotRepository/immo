from Model.DB.db import *
from Controller.controller import *

"""MVC example:
https://gist.github.com/ajfigueroa/c2af555630d1db3efb5178ece728b017"""

if __name__ == "__main__":
    my_controller = Controller(fake=True, skip_parse=True)
