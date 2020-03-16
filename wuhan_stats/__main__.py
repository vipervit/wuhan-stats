import os
import sys
import time
import logging
import getopt

from tkinter import *

from wuhan_stats import __version__, logger, EMAIL_ATTRIBS
from wuhan_stats.src.app import Application

if __name__ == '__main__':

    if not __debug__:
        logger.setLevel(logging.DEBUG)

    try:
        opts, args = getopt.getopt(sys.argv[1:], 't:f:s:u:', [])
    except getopt.GetoptError as err:
        logger.error(err)
        logger.info(__doc__)
        sys.exit(2)

    for opt, args in opts:
        if opt == '-t':
            EMAIL_ATTRIBS.to = args
        if opt == '-f':
            EMAIL_ATTRIBS.from_ = args
        if opt == '-s':
            EMAIL_ATTRIBS.keyring_service = args
        if opt == '-u':
            EMAIL_ATTRIBS.keyring_uid = args

    root = Tk()
    root.title('COVID-19   v.' + __version__)
    app = Application(master=root)
    app.mainloop()
    root.destroy()
