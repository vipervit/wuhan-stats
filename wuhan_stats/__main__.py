import os
import sys
import time
import logging
import getopt

from tkinter import *

from wuhan_stats import __version__, logger
from wuhan_stats.src.app import Application

logger = logging.getLogger(__name__)

if __name__ == '__main__':

    try:
        opts, args = getopt.getopt(sys.argv[1:], 'd', [])
    except getopt.GetoptError as err:
        logger.error(err)
        logger.info(__doc__)
        sys.exit(2)

    for opt, args in opts:
        if opt == '-d':
            logger.setLevel(logging.DEBUG)

    root = Tk()
    root.title('COVID-19')
    app = Application(master=root)
    app.mainloop()
    root.destroy()
