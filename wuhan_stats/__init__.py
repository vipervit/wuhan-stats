import logging

logger = logging.getLogger(__name__)
console = logging.StreamHandler()
logger.addHandler(console)

__version__ = '1.7'
