import os
import sys
import time
import logging
import getopt

from tkinter import *

from wuhan_stats import __version__, logger
from wuhan_stats.src.app import Application

if __name__ == '__main__':

    if not __debug__:
        logger.setLevel(logging.DEBUG)

    root = Tk()
    root.title('COVID-19   v.' + __version__)
    app = Application(master=root)
    app.mainloop()
    root.destroy()
