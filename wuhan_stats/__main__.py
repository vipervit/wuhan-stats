import os
import sys
import time
import logging

from wuhan_stats import __version__, logger, SLEEP, SLEEP_MIN
from wuhan_stats.src.site import site as site

if not __debug__:
    logger.setLevel(logging.DEBUG)


def main():
    if SLEEP < SLEEP_MIN: # to restrict polling period in order not to abuse the sources
        logger.data('Polling period may not be less than ' + SLEEP_MIN + ' min.')
        raise SystemExit
    prev = ''
    while True:
        with site('Worldometer') as worldometer:
            worldometer.get()
            if prev < worldometer.last_updated:
                worldometer.desktop.send()
                worldometer.email.send()
                prev = worldometer.last_updated
            if not __debug__:
                logger.debug('Exiting due to debug mode.')
                sys.exit()
            time.sleep(SLEEP)

if __name__ == '__main__':
    main()
