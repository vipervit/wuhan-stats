import logging

__version__ = '1.18.01'

logger = logging.getLogger(__name__)
console = logging.StreamHandler()
logger.addHandler(console)
