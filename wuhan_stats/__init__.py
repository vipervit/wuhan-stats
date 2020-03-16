import logging

logger = logging.getLogger(__name__)
console = logging.StreamHandler()
logger.addHandler(console)

__version__ = '1.7.75'

PERIOD_DEFAULT = 1 # hours
PERIOD_MIN = 0.25 # hours
WIN_NOTIFICATION_TIMEOUT = 3600

SITES = { 'Worldometer': {'home': 'https://www.worldometers.info', 'updates': '/coronavirus/'} } # Other sources may be added in the future
